"""Backtesting API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd

from ..backtest.engine import BacktestEngine
from ..strategies.momentum import MomentumBreakoutStrategy
from ..strategies.mean_reversion import MeanReversionRSIStrategy
from .auth import get_current_client

router = APIRouter()


class BacktestRequest(BaseModel):
    strategy_type: str
    symbols: List[str]
    parameters: Dict[str, Any]
    start_date: str
    end_date: str
    initial_capital: float = 100000.0


class BacktestResult(BaseModel):
    total_return: float
    buy_and_hold_return: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    avg_trade_duration_days: float
    sharpe_ratio: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    equity_curve: List[Dict[str, Any]]


@router.post("/run", response_model=BacktestResult)
async def run_backtest(request: BacktestRequest):
    """
    Run a backtest on historical data with realistic execution simulation
    """
    try:
        # Get authenticated client
        client = get_current_client()

        # Parse dates
        start_date = datetime.fromisoformat(request.start_date)
        end_date = datetime.fromisoformat(request.end_date)

        # Create strategy instance
        strategy = _create_strategy(
            request.strategy_type,
            request.symbols,
            request.parameters
        )

        if strategy is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown strategy type: {request.strategy_type}"
            )

        # Fetch historical data
        market_data = {}
        for symbol in request.symbols:
            try:
                bars = client.get_bars(
                    symbol=symbol,
                    timeframe="1day",
                    start=start_date - timedelta(days=200),  # Extra data for indicators
                    end=end_date
                )

                if bars:
                    df = pd.DataFrame(bars)
                    df["timestamp"] = pd.to_datetime(df["timestamp"])
                    df.set_index("timestamp", inplace=True)
                    market_data[symbol] = df
                else:
                    raise Exception(f"No data available for {symbol}")

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch data for {symbol}: {str(e)}"
                )

        # Create backtest engine
        engine = BacktestEngine(
            initial_capital=request.initial_capital,
            slippage_pct=0.05,  # 0.05% average slippage
        )

        # Run backtest
        metrics, equity_curve = engine.run(
            strategy=strategy,
            market_data=market_data,
            start_date=start_date,
            end_date=end_date
        )

        # Format result
        result = BacktestResult(
            total_return=metrics.total_return,
            buy_and_hold_return=metrics.buy_and_hold_return,
            max_drawdown=metrics.max_drawdown,
            win_rate=metrics.win_rate,
            total_trades=metrics.total_trades,
            winning_trades=metrics.winning_trades,
            losing_trades=metrics.losing_trades,
            avg_win=metrics.avg_win,
            avg_loss=metrics.avg_loss,
            avg_trade_duration_days=metrics.avg_trade_duration_days,
            sharpe_ratio=metrics.sharpe_ratio,
            max_consecutive_wins=metrics.max_consecutive_wins,
            max_consecutive_losses=metrics.max_consecutive_losses,
            equity_curve=equity_curve,
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")


def _create_strategy(strategy_type: str, symbols: List[str], parameters: Dict[str, Any]):
    """Create strategy instance based on type"""
    strategy_map = {
        "momentum_breakout": MomentumBreakoutStrategy,
        "mean_reversion_rsi": MeanReversionRSIStrategy,
    }

    strategy_class = strategy_map.get(strategy_type)
    if strategy_class:
        return strategy_class(symbols, parameters)

    return None


@router.get("/templates")
async def get_backtest_templates():
    """
    Get example backtest configurations
    """
    return {
        "templates": [
            {
                "name": "Momentum Backtest - SPY 5 Years",
                "strategy_type": "momentum_breakout",
                "symbols": ["SPY"],
                "parameters": {
                    "lookback_period": 20,
                    "volume_multiplier": 1.5,
                    "position_size_pct": 10,
                },
                "start_date": (datetime.now() - timedelta(days=365*5)).isoformat(),
                "end_date": datetime.now().isoformat(),
            },
            {
                "name": "Mean Reversion - Tech Stocks",
                "strategy_type": "mean_reversion_rsi",
                "symbols": ["AAPL", "MSFT", "GOOGL"],
                "parameters": {
                    "rsi_period": 14,
                    "rsi_oversold": 30,
                    "rsi_overbought": 70,
                },
                "start_date": (datetime.now() - timedelta(days=365*2)).isoformat(),
                "end_date": datetime.now().isoformat(),
            },
        ]
    }
