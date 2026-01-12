"""Database models"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import json

from .database import Base


class Strategy(Base):
    """
    Stored trading strategy
    """
    __tablename__ = "strategies"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # momentum_breakout, mean_reversion_rsi, etc.
    symbols = Column(Text, nullable=False)  # JSON array of symbols
    parameters = Column(Text, nullable=False)  # JSON dict of parameters
    enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    executions = relationship("StrategyExecution", back_populates="strategy", cascade="all, delete-orphan")
    backtests = relationship("BacktestResult", back_populates="strategy", cascade="all, delete-orphan")

    def get_symbols_list(self):
        """Parse symbols from JSON"""
        return json.loads(self.symbols)

    def set_symbols_list(self, symbols_list):
        """Set symbols as JSON"""
        self.symbols = json.dumps(symbols_list)

    def get_parameters_dict(self):
        """Parse parameters from JSON"""
        return json.loads(self.parameters)

    def set_parameters_dict(self, params_dict):
        """Set parameters as JSON"""
        self.parameters = json.dumps(params_dict)


class StrategyExecution(Base):
    """
    Record of strategy execution
    """
    __tablename__ = "strategy_executions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(String, ForeignKey("strategies.id"), nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)
    signals_generated = Column(Integer, default=0)
    orders_placed = Column(Integer, default=0)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)

    # Relationship
    strategy = relationship("Strategy", back_populates="executions")


class BacktestResult(Base):
    """
    Stored backtest results
    """
    __tablename__ = "backtest_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(String, ForeignKey("strategies.id"), nullable=True)
    strategy_type = Column(String, nullable=False)
    symbols = Column(Text, nullable=False)  # JSON array
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    initial_capital = Column(Float, nullable=False)

    # Metrics
    total_return = Column(Float, nullable=False)
    buy_and_hold_return = Column(Float, nullable=False)
    max_drawdown = Column(Float, nullable=False)
    sharpe_ratio = Column(Float, nullable=False)
    win_rate = Column(Float, nullable=False)
    total_trades = Column(Integer, nullable=False)
    winning_trades = Column(Integer, nullable=False)
    losing_trades = Column(Integer, nullable=False)
    avg_win = Column(Float, nullable=False)
    avg_loss = Column(Float, nullable=False)
    avg_trade_duration_days = Column(Float, nullable=False)
    max_consecutive_wins = Column(Integer, nullable=False)
    max_consecutive_losses = Column(Integer, nullable=False)

    # Equity curve (stored as JSON)
    equity_curve = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    strategy = relationship("Strategy", back_populates="backtests")

    def get_equity_curve_list(self):
        """Parse equity curve from JSON"""
        return json.loads(self.equity_curve)

    def set_equity_curve_list(self, curve_list):
        """Set equity curve as JSON"""
        self.equity_curve = json.dumps(curve_list)


class Order(Base):
    """
    Stored order records
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alpaca_order_id = Column(String, unique=True, nullable=False)
    strategy_id = Column(String, ForeignKey("strategies.id"), nullable=True)
    symbol = Column(String, nullable=False)
    qty = Column(Float, nullable=False)
    side = Column(String, nullable=False)  # buy, sell
    type = Column(String, nullable=False)  # market, limit, etc.
    status = Column(String, nullable=False)
    submitted_at = Column(DateTime, nullable=False)
    filled_at = Column(DateTime, nullable=True)
    filled_avg_price = Column(Float, nullable=True)
    filled_qty = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Position(Base):
    """
    Position snapshots for tracking
    """
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False)
    qty = Column(Float, nullable=False)
    avg_entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    market_value = Column(Float, nullable=False)
    cost_basis = Column(Float, nullable=False)
    unrealized_pl = Column(Float, nullable=False)
    unrealized_plpc = Column(Float, nullable=False)

    snapshot_at = Column(DateTime, default=datetime.utcnow)


class PortfolioSnapshot(Base):
    """
    Daily portfolio value snapshots
    """
    __tablename__ = "portfolio_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_value = Column(Float, nullable=False)
    cash = Column(Float, nullable=False)
    equity = Column(Float, nullable=False)
    buying_power = Column(Float, nullable=False)

    snapshot_at = Column(DateTime, default=datetime.utcnow)
