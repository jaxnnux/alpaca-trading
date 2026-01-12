"""Backtesting engine with realistic execution simulation"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import pandas as pd
import numpy as np

from ..strategies.base import BaseStrategy, Signal
from ..brokers.alpaca import AlpacaBroker


@dataclass
class BacktestOrder:
    """Represents an order in the backtest"""
    symbol: str
    qty: float
    side: str  # 'buy' or 'sell'
    entry_price: float
    entry_date: datetime
    exit_price: Optional[float] = None
    exit_date: Optional[datetime] = None
    pnl: float = 0.0
    pnl_pct: float = 0.0


@dataclass
class BacktestMetrics:
    """Backtest performance metrics"""
    total_return: float
    buy_and_hold_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    avg_trade_duration_days: float
    max_consecutive_wins: int
    max_consecutive_losses: int


class BacktestEngine:
    """
    Backtesting engine with realistic execution modeling

    Features:
    - Simulates historical strategy execution
    - Models slippage and trading costs
    - Calculates comprehensive performance metrics
    - Generates equity curve
    """

    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission_per_trade: float = 0.0,  # Alpaca is commission-free
        slippage_pct: float = 0.05,  # 0.05% average slippage
    ):
        self.initial_capital = initial_capital
        self.commission = commission_per_trade
        self.slippage_pct = slippage_pct

        self.cash = initial_capital
        self.equity = initial_capital
        self.positions: List[BacktestOrder] = []
        self.closed_trades: List[BacktestOrder] = []
        self.equity_curve: List[Dict[str, Any]] = []

    def run(
        self,
        strategy: BaseStrategy,
        market_data: Dict[str, pd.DataFrame],
        start_date: datetime,
        end_date: datetime,
    ) -> tuple[BacktestMetrics, List[Dict[str, Any]]]:
        """
        Run backtest for a strategy

        Args:
            strategy: Strategy to backtest
            market_data: Historical market data for all symbols
            start_date: Start date for backtest
            end_date: End date for backtest

        Returns:
            Tuple of (metrics, equity_curve)
        """
        # Reset state
        self.cash = self.initial_capital
        self.equity = self.initial_capital
        self.positions = []
        self.closed_trades = []
        self.equity_curve = []

        # Get trading days
        trading_days = self._get_trading_days(market_data, start_date, end_date)

        # Iterate through each trading day
        for current_date in trading_days:
            # Get market data up to current date
            historical_data = self._get_historical_data(market_data, start_date, current_date)

            # Generate signals
            signals = strategy.analyze(historical_data)

            # Execute signals
            for signal in signals:
                self._execute_signal(signal, current_date, market_data)

            # Update portfolio value
            self._update_portfolio_value(current_date, market_data)

            # Record equity
            self.equity_curve.append({
                "date": current_date.isoformat(),
                "equity": self.equity,
                "cash": self.cash,
                "positions_value": self.equity - self.cash,
                "profit_loss": self.equity - self.initial_capital,
                "profit_loss_pct": ((self.equity - self.initial_capital) / self.initial_capital) * 100,
            })

        # Calculate metrics
        metrics = self._calculate_metrics(market_data, start_date, end_date)

        return metrics, self.equity_curve

    def _get_trading_days(
        self,
        market_data: Dict[str, pd.DataFrame],
        start_date: datetime,
        end_date: datetime,
    ) -> List[datetime]:
        """Get all trading days in the date range"""
        # Use the first symbol's data to get trading days
        if not market_data:
            return []

        first_symbol = list(market_data.keys())[0]
        df = market_data[first_symbol]

        # Filter by date range
        mask = (df.index >= start_date) & (df.index <= end_date)
        trading_days = df[mask].index.tolist()

        return trading_days

    def _get_historical_data(
        self,
        market_data: Dict[str, pd.DataFrame],
        start_date: datetime,
        current_date: datetime,
    ) -> Dict[str, pd.DataFrame]:
        """Get market data up to current date"""
        historical = {}

        for symbol, df in market_data.items():
            mask = (df.index >= start_date) & (df.index <= current_date)
            historical[symbol] = df[mask].copy()

        return historical

    def _execute_signal(
        self,
        signal: Signal,
        current_date: datetime,
        market_data: Dict[str, pd.DataFrame],
    ):
        """Execute a trading signal"""
        symbol = signal.symbol

        # Get current price
        if symbol not in market_data:
            return

        try:
            current_price = market_data[symbol].loc[current_date, "close"]
        except KeyError:
            return

        if signal.action == "buy":
            # Apply slippage (buy at slightly higher price)
            execution_price = current_price * (1 + self.slippage_pct / 100)

            # Calculate position size
            position_cost = execution_price * signal.quantity

            if position_cost <= self.cash:
                # Open position
                self.cash -= position_cost + self.commission

                order = BacktestOrder(
                    symbol=symbol,
                    qty=signal.quantity,
                    side="buy",
                    entry_price=execution_price,
                    entry_date=current_date,
                )

                self.positions.append(order)

        elif signal.action == "sell":
            # Close matching positions
            self._close_positions(symbol, current_date, market_data)

    def _close_positions(
        self,
        symbol: str,
        current_date: datetime,
        market_data: Dict[str, pd.DataFrame],
    ):
        """Close all positions for a symbol"""
        try:
            current_price = market_data[symbol].loc[current_date, "close"]
        except KeyError:
            return

        # Apply slippage (sell at slightly lower price)
        execution_price = current_price * (1 - self.slippage_pct / 100)

        # Find and close all positions for this symbol
        positions_to_close = [p for p in self.positions if p.symbol == symbol]

        for position in positions_to_close:
            # Calculate P&L
            pnl = (execution_price - position.entry_price) * position.qty
            pnl -= self.commission
            pnl_pct = ((execution_price - position.entry_price) / position.entry_price) * 100

            # Update position
            position.exit_price = execution_price
            position.exit_date = current_date
            position.pnl = pnl
            position.pnl_pct = pnl_pct

            # Update cash
            self.cash += (execution_price * position.qty) - self.commission

            # Move to closed trades
            self.closed_trades.append(position)
            self.positions.remove(position)

    def _update_portfolio_value(
        self,
        current_date: datetime,
        market_data: Dict[str, pd.DataFrame],
    ):
        """Update total portfolio value"""
        positions_value = 0.0

        for position in self.positions:
            try:
                current_price = market_data[position.symbol].loc[current_date, "close"]
                positions_value += current_price * position.qty
            except KeyError:
                # Use entry price if no current data
                positions_value += position.entry_price * position.qty

        self.equity = self.cash + positions_value

    def _calculate_metrics(
        self,
        market_data: Dict[str, pd.DataFrame],
        start_date: datetime,
        end_date: datetime,
    ) -> BacktestMetrics:
        """Calculate backtest performance metrics"""
        # Total return
        total_return = ((self.equity - self.initial_capital) / self.initial_capital) * 100

        # Buy and hold return (using first symbol)
        buy_hold_return = 0.0
        if market_data:
            first_symbol = list(market_data.keys())[0]
            df = market_data[first_symbol]

            try:
                start_price = df.loc[start_date, "close"]
                end_price = df.loc[end_date, "close"]
                buy_hold_return = ((end_price - start_price) / start_price) * 100
            except KeyError:
                pass

        # Win rate and trade stats
        winning_trades = [t for t in self.closed_trades if t.pnl > 0]
        losing_trades = [t for t in self.closed_trades if t.pnl <= 0]

        total_trades = len(self.closed_trades)
        win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0

        avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0

        # Average trade duration
        durations = []
        for trade in self.closed_trades:
            if trade.exit_date:
                duration = (trade.exit_date - trade.entry_date).days
                durations.append(duration)

        avg_duration = np.mean(durations) if durations else 0

        # Max drawdown
        max_dd = self._calculate_max_drawdown()

        # Sharpe ratio (simplified)
        sharpe = self._calculate_sharpe_ratio()

        # Consecutive wins/losses
        max_consec_wins, max_consec_losses = self._calculate_consecutive_trades()

        return BacktestMetrics(
            total_return=total_return,
            buy_and_hold_return=buy_hold_return,
            max_drawdown=max_dd,
            sharpe_ratio=sharpe,
            win_rate=win_rate,
            total_trades=total_trades,
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            avg_win=avg_win,
            avg_loss=avg_loss,
            avg_trade_duration_days=avg_duration,
            max_consecutive_wins=max_consec_wins,
            max_consecutive_losses=max_consec_losses,
        )

    def _calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown percentage"""
        if not self.equity_curve:
            return 0.0

        equity_values = [point["equity"] for point in self.equity_curve]
        peak = equity_values[0]
        max_dd = 0.0

        for value in equity_values:
            if value > peak:
                peak = value

            dd = ((peak - value) / peak) * 100
            if dd > max_dd:
                max_dd = dd

        return -max_dd  # Return as negative

    def _calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio (simplified)"""
        if len(self.equity_curve) < 2:
            return 0.0

        returns = []
        for i in range(1, len(self.equity_curve)):
            prev_equity = self.equity_curve[i - 1]["equity"]
            curr_equity = self.equity_curve[i]["equity"]
            ret = (curr_equity - prev_equity) / prev_equity
            returns.append(ret)

        if not returns:
            return 0.0

        avg_return = np.mean(returns)
        std_return = np.std(returns)

        if std_return == 0:
            return 0.0

        # Annualize (assuming daily returns)
        sharpe = (avg_return / std_return) * np.sqrt(252)

        return sharpe

    def _calculate_consecutive_trades(self) -> tuple[int, int]:
        """Calculate max consecutive wins and losses"""
        if not self.closed_trades:
            return 0, 0

        max_wins = 0
        max_losses = 0
        current_wins = 0
        current_losses = 0

        for trade in self.closed_trades:
            if trade.pnl > 0:
                current_wins += 1
                current_losses = 0
                max_wins = max(max_wins, current_wins)
            else:
                current_losses += 1
                current_wins = 0
                max_losses = max(max_losses, current_losses)

        return max_wins, max_losses
