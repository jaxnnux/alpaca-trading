"""Strategy execution scheduler"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd

from ..strategies.base import BaseStrategy, Signal
from ..strategies.momentum import MomentumBreakoutStrategy
from ..strategies.mean_reversion import MeanReversionRSIStrategy
from ..brokers.alpaca import AlpacaBroker
from .position_monitor import PositionMonitor


class StrategyScheduler:
    """
    Manages periodic execution of trading strategies

    Features:
    - Evaluates strategies at configured intervals
    - Fetches market data for analysis
    - Generates and executes trading signals
    - Tracks strategy performance
    """

    def __init__(self, broker: AlpacaBroker):
        self.broker = broker
        self.strategies: Dict[str, Dict] = {}  # strategy_id -> strategy config
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.is_running = False
        self.open_positions: Dict[str, float] = {}  # symbol -> quantity (track positions)
        self.position_monitor = PositionMonitor(broker, check_interval_seconds=10)  # Check SL/TP every 10 seconds

    def add_strategy(
        self,
        strategy_id: str,
        strategy_type: str,
        symbols: List[str],
        parameters: Dict,
        interval_seconds: int = 60,
    ):
        """
        Add a strategy to the scheduler

        Args:
            strategy_id: Unique identifier for the strategy
            strategy_type: Type of strategy (momentum, mean_reversion, etc.)
            symbols: List of symbols to trade
            parameters: Strategy-specific parameters
            interval_seconds: How often to evaluate the strategy (default: 60s)
        """
        # Create strategy instance
        strategy = self._create_strategy(strategy_type, symbols, parameters)

        if strategy is None:
            raise ValueError(f"Unknown strategy type: {strategy_type}")

        self.strategies[strategy_id] = {
            "strategy": strategy,
            "type": strategy_type,
            "symbols": symbols,
            "parameters": parameters,
            "interval": interval_seconds,
            "enabled": False,
            "last_execution": None,
            "executions": 0,
            "signals_generated": 0,
            "orders_placed": 0,
        }

    def _create_strategy(
        self, strategy_type: str, symbols: List[str], parameters: Dict
    ) -> Optional[BaseStrategy]:
        """Create strategy instance based on type"""
        strategy_map = {
            "momentum_breakout": MomentumBreakoutStrategy,
            "mean_reversion_rsi": MeanReversionRSIStrategy,
        }

        strategy_class = strategy_map.get(strategy_type)
        if strategy_class:
            return strategy_class(symbols, parameters)

        return None

    def enable_strategy(self, strategy_id: str):
        """Enable a strategy"""
        if strategy_id not in self.strategies:
            raise ValueError(f"Strategy not found: {strategy_id}")

        self.strategies[strategy_id]["enabled"] = True

        # Start execution task if scheduler is running
        if self.is_running and strategy_id not in self.active_tasks:
            self.active_tasks[strategy_id] = asyncio.create_task(
                self._run_strategy_loop(strategy_id)
            )

    def disable_strategy(self, strategy_id: str):
        """Disable a strategy"""
        if strategy_id not in self.strategies:
            raise ValueError(f"Strategy not found: {strategy_id}")

        self.strategies[strategy_id]["enabled"] = False

        # Cancel execution task
        if strategy_id in self.active_tasks:
            self.active_tasks[strategy_id].cancel()
            del self.active_tasks[strategy_id]

    def remove_strategy(self, strategy_id: str):
        """Remove a strategy from the scheduler"""
        if strategy_id in self.strategies:
            self.disable_strategy(strategy_id)
            del self.strategies[strategy_id]

    async def start(self):
        """Start the scheduler"""
        self.is_running = True

        # Start position monitor
        await self.position_monitor.start()

        # Start tasks for all enabled strategies
        for strategy_id, config in self.strategies.items():
            if config["enabled"] and strategy_id not in self.active_tasks:
                self.active_tasks[strategy_id] = asyncio.create_task(
                    self._run_strategy_loop(strategy_id)
                )

    async def stop(self):
        """Stop the scheduler"""
        self.is_running = False

        # Stop position monitor
        await self.position_monitor.stop()

        # Cancel all active tasks
        for task in self.active_tasks.values():
            task.cancel()

        self.active_tasks.clear()

    async def _run_strategy_loop(self, strategy_id: str):
        """
        Main execution loop for a strategy
        """
        config = self.strategies[strategy_id]
        strategy: BaseStrategy = config["strategy"]
        interval = config["interval"]

        while self.is_running and config["enabled"]:
            try:
                # Execute strategy
                await self._execute_strategy(strategy_id, strategy, config)

                # Wait for next execution
                await asyncio.sleep(interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error executing strategy {strategy_id}: {e}")
                # Wait before retrying
                await asyncio.sleep(interval)

    async def _execute_strategy(
        self, strategy_id: str, strategy: BaseStrategy, config: Dict
    ):
        """
        Execute a single strategy iteration
        """
        # Update execution stats
        config["last_execution"] = datetime.utcnow()
        config["executions"] += 1

        # Check position monitor for stop-loss/take-profit signals FIRST
        monitor_signals = await self.position_monitor.check_positions()
        if monitor_signals:
            print(f"Position monitor generated {len(monitor_signals)} exit signals")
            for signal in monitor_signals:
                try:
                    await self._execute_signal(signal)
                    config["orders_placed"] += 1
                except Exception as e:
                    print(f"Failed to execute monitor signal for {signal.symbol}: {e}")

        # Sync open positions from broker
        self._sync_positions()

        # Get current portfolio value for position sizing
        try:
            account = self.broker.get_account()
            portfolio_value = float(account.get("equity", 0))
        except Exception as e:
            print(f"Failed to get account info: {e}")
            portfolio_value = None  # Strategy will handle None gracefully

        # Fetch market data for all symbols
        market_data = await self._fetch_market_data(
            config["symbols"], lookback_days=100
        )

        # Generate signals with portfolio value for proper position sizing
        signals: List[Signal] = strategy.analyze(market_data, portfolio_value)

        if signals:
            config["signals_generated"] += len(signals)

            # Execute signals
            for signal in signals:
                try:
                    await self._execute_signal(signal)
                    config["orders_placed"] += 1
                except Exception as e:
                    print(f"Failed to execute signal for {signal.symbol}: {e}")

    async def _fetch_market_data(
        self, symbols: List[str], lookback_days: int = 100
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch historical market data for analysis
        """
        market_data = {}

        end = datetime.utcnow()
        start = end - timedelta(days=lookback_days)

        for symbol in symbols:
            try:
                bars = self.broker.get_bars(symbol, "1day", start, end)

                if bars:
                    df = pd.DataFrame(bars)
                    df["timestamp"] = pd.to_datetime(df["timestamp"])
                    df.set_index("timestamp", inplace=True)
                    market_data[symbol] = df
                else:
                    market_data[symbol] = pd.DataFrame()

            except Exception as e:
                print(f"Failed to fetch data for {symbol}: {e}")
                market_data[symbol] = pd.DataFrame()

        return market_data

    def _sync_positions(self):
        """
        Sync open positions from broker to track for sell orders
        """
        try:
            positions = self.broker.get_positions()
            self.open_positions = {
                pos["symbol"]: float(pos["qty"])
                for pos in positions
            }
        except Exception as e:
            print(f"Failed to sync positions: {e}")
            # Keep existing position data if sync fails

    async def _execute_signal(self, signal: Signal):
        """
        Execute a trading signal by placing an order
        """
        if signal.action == "buy":
            # Place buy order
            self.broker.submit_order(
                symbol=signal.symbol,
                qty=signal.quantity,
                side="buy",
                order_type="market",
                time_in_force="day",
            )
            print(f"BUY {signal.quantity} {signal.symbol}: {signal.reason}")

            # Track position (update on buy)
            self.open_positions[signal.symbol] = self.open_positions.get(signal.symbol, 0) + signal.quantity

            # Add to position monitor for stop-loss/take-profit tracking
            if signal.metadata:
                entry_price = signal.metadata.get("entry_price")
                stop_loss = signal.metadata.get("stop_loss")
                take_profit = signal.metadata.get("take_profit")

                if entry_price and (stop_loss or take_profit):
                    self.position_monitor.add_position(
                        symbol=signal.symbol,
                        quantity=signal.quantity,
                        entry_price=entry_price,
                        stop_loss=stop_loss,
                        take_profit=take_profit
                    )

        elif signal.action == "sell":
            # Get actual position quantity
            if signal.quantity > 0:
                # Specific quantity provided
                sell_qty = signal.quantity
            else:
                # Sell entire position (quantity = 0 means "sell all")
                sell_qty = self.open_positions.get(signal.symbol, 0)

                if sell_qty == 0:
                    print(f"SKIP SELL {signal.symbol}: No position held")
                    return

            # Place sell order
            self.broker.submit_order(
                symbol=signal.symbol,
                qty=sell_qty,
                side="sell",
                order_type="market",
                time_in_force="day",
            )
            print(f"SELL {sell_qty} {signal.symbol}: {signal.reason}")

            # Update tracked position
            current_qty = self.open_positions.get(signal.symbol, 0)
            new_qty = max(0, current_qty - sell_qty)
            if new_qty == 0:
                self.open_positions.pop(signal.symbol, None)
                # Remove from position monitor when fully closed
                self.position_monitor.remove_position(signal.symbol)
            else:
                self.open_positions[signal.symbol] = new_qty
                # Update quantity in position monitor
                self.position_monitor.update_position_quantity(signal.symbol, new_qty)

    def get_status(self) -> Dict:
        """
        Get scheduler status and statistics
        """
        return {
            "is_running": self.is_running,
            "active_strategies": len([s for s in self.strategies.values() if s["enabled"]]),
            "total_strategies": len(self.strategies),
            "strategies": {
                sid: {
                    "type": config["type"],
                    "enabled": config["enabled"],
                    "symbols": config["symbols"],
                    "interval": config["interval"],
                    "last_execution": config["last_execution"].isoformat() if config["last_execution"] else None,
                    "executions": config["executions"],
                    "signals_generated": config["signals_generated"],
                    "orders_placed": config["orders_placed"],
                }
                for sid, config in self.strategies.items()
            },
        }
