"""Position monitoring service for stop-loss and take-profit management"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

from ..strategies.base import Signal
from ..brokers.alpaca import AlpacaBroker


@dataclass
class MonitoredPosition:
    """Position being monitored for stop-loss/take-profit"""
    symbol: str
    quantity: float
    entry_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    entry_time: datetime = None

    def __post_init__(self):
        if self.entry_time is None:
            self.entry_time = datetime.utcnow()


class PositionMonitor:
    """
    Monitors open positions for stop-loss and take-profit levels

    Features:
    - Tracks positions with entry prices
    - Monitors current prices via WebSocket or polling
    - Generates automatic sell signals when SL/TP breached
    - Configurable check interval
    """

    def __init__(self, broker: AlpacaBroker, check_interval_seconds: int = 5):
        self.broker = broker
        self.check_interval = check_interval_seconds
        self.monitored_positions: Dict[str, MonitoredPosition] = {}
        self.is_running = False
        self.monitor_task: Optional[asyncio.Task] = None

    def add_position(
        self,
        symbol: str,
        quantity: float,
        entry_price: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ):
        """
        Add a position to monitor for stop-loss/take-profit

        Args:
            symbol: Stock symbol
            quantity: Number of shares
            entry_price: Entry price
            stop_loss: Stop loss price (optional)
            take_profit: Take profit price (optional)
        """
        self.monitored_positions[symbol] = MonitoredPosition(
            symbol=symbol,
            quantity=quantity,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        print(f"Monitoring {symbol}: entry={entry_price:.2f}, SL={stop_loss:.2f if stop_loss else 'None'}, TP={take_profit:.2f if take_profit else 'None'}")

    def remove_position(self, symbol: str):
        """Remove a position from monitoring"""
        if symbol in self.monitored_positions:
            del self.monitored_positions[symbol]
            print(f"Stopped monitoring {symbol}")

    def update_position_quantity(self, symbol: str, new_quantity: float):
        """Update the quantity of a monitored position"""
        if symbol in self.monitored_positions:
            if new_quantity <= 0:
                self.remove_position(symbol)
            else:
                self.monitored_positions[symbol].quantity = new_quantity

    async def start(self):
        """Start the position monitoring loop"""
        if self.is_running:
            print("Position monitor already running")
            return

        self.is_running = True
        self.monitor_task = asyncio.create_task(self._monitor_loop())
        print("Position monitor started")

    async def stop(self):
        """Stop the position monitoring loop"""
        self.is_running = False
        if self.monitor_task:
            self.monitor_task.cancel()
            self.monitor_task = None
        print("Position monitor stopped")

    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                # Check all monitored positions
                signals = await self._check_positions()

                # Yield signals for execution (caller must handle)
                if signals:
                    for signal in signals:
                        print(f"Position monitor generated signal: {signal.action} {signal.symbol} - {signal.reason}")
                        # Note: Signals are returned by check_positions() for external handling

                # Wait before next check
                await asyncio.sleep(self.check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in position monitor loop: {e}")
                await asyncio.sleep(self.check_interval)

    async def check_positions(self) -> List[Signal]:
        """
        Check all monitored positions and return exit signals

        This method can be called externally by the scheduler

        Returns:
            List of sell signals for positions that breached SL/TP
        """
        return await self._check_positions()

    async def _check_positions(self) -> List[Signal]:
        """
        Check monitored positions against current prices

        Returns:
            List of sell signals for positions that need to exit
        """
        signals = []

        if not self.monitored_positions:
            return signals

        # Get current prices for all monitored symbols
        symbols = list(self.monitored_positions.keys())

        for symbol in symbols:
            position = self.monitored_positions[symbol]

            try:
                # Get current price
                current_price = await self._get_current_price(symbol)

                if current_price is None:
                    continue

                # Check stop loss
                if position.stop_loss and current_price <= position.stop_loss:
                    signals.append(Signal(
                        symbol=symbol,
                        action="sell",
                        quantity=position.quantity,
                        reason=f"Stop loss triggered: price {current_price:.2f} <= SL {position.stop_loss:.2f}",
                        metadata={
                            "exit_price": current_price,
                            "entry_price": position.entry_price,
                            "stop_loss": position.stop_loss,
                            "pnl_pct": ((current_price - position.entry_price) / position.entry_price) * 100
                        }
                    ))
                    # Remove from monitoring after generating signal
                    self.remove_position(symbol)
                    continue

                # Check take profit
                if position.take_profit and current_price >= position.take_profit:
                    signals.append(Signal(
                        symbol=symbol,
                        action="sell",
                        quantity=position.quantity,
                        reason=f"Take profit triggered: price {current_price:.2f} >= TP {position.take_profit:.2f}",
                        metadata={
                            "exit_price": current_price,
                            "entry_price": position.entry_price,
                            "take_profit": position.take_profit,
                            "pnl_pct": ((current_price - position.entry_price) / position.entry_price) * 100
                        }
                    ))
                    # Remove from monitoring after generating signal
                    self.remove_position(symbol)
                    continue

            except Exception as e:
                print(f"Error checking position for {symbol}: {e}")
                continue

        return signals

    async def _get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for a symbol

        Args:
            symbol: Stock symbol

        Returns:
            Current price or None if unavailable
        """
        try:
            # Try to get latest quote
            quote = self.broker.get_latest_quote(symbol)
            if quote:
                # Use mid price between bid and ask
                bid = float(quote.get("bid_price", 0))
                ask = float(quote.get("ask_price", 0))
                if bid > 0 and ask > 0:
                    return (bid + ask) / 2
                elif ask > 0:
                    return ask
                elif bid > 0:
                    return bid

            # Fallback: get latest trade price
            trade = self.broker.get_latest_trade(symbol)
            if trade:
                return float(trade.get("price", 0))

            return None

        except Exception as e:
            print(f"Failed to get current price for {symbol}: {e}")
            return None

    def get_monitored_positions(self) -> Dict[str, Dict]:
        """
        Get all monitored positions

        Returns:
            Dictionary of symbol -> position details
        """
        return {
            symbol: {
                "quantity": pos.quantity,
                "entry_price": pos.entry_price,
                "stop_loss": pos.stop_loss,
                "take_profit": pos.take_profit,
                "entry_time": pos.entry_time.isoformat() if pos.entry_time else None
            }
            for symbol, pos in self.monitored_positions.items()
        }

    def get_status(self) -> Dict:
        """Get monitor status"""
        return {
            "is_running": self.is_running,
            "monitored_count": len(self.monitored_positions),
            "check_interval_seconds": self.check_interval,
            "positions": list(self.monitored_positions.keys())
        }
