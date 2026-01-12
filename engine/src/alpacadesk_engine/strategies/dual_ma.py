"""Dual Moving Average Crossover Strategy"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np

from .base import BaseStrategy, Signal


class DualMovingAverageStrategy(BaseStrategy):
    """
    Dual Moving Average Crossover Strategy

    Buy when fast MA crosses above slow MA (golden cross).
    Sell when fast MA crosses below slow MA (death cross).

    Parameters:
    - fast_ma: Fast moving average period (default: 50)
    - slow_ma: Slow moving average period (default: 200)
    - trend_ma: Trend filter MA period (default: 20)
    - position_size_pct: Percentage of portfolio to allocate (default: 20)
    """

    def __init__(self, symbols: List[str], parameters: Dict[str, Any]):
        default_params = {
            "fast_ma": 50,
            "slow_ma": 200,
            "trend_ma": 20,
            "position_size_pct": 20,
        }
        default_params.update(parameters)

        super().__init__(
            name="Dual Moving Average",
            symbols=symbols,
            parameters=default_params,
        )

    def analyze(self, market_data: Dict[str, pd.DataFrame]) -> List[Signal]:
        """
        Generate trading signals based on MA crossover logic
        """
        signals = []

        for symbol in self.symbols:
            if symbol not in market_data or market_data[symbol].empty:
                continue

            df = market_data[symbol].copy()

            # Calculate moving averages
            fast_ma = self.parameters["fast_ma"]
            slow_ma = self.parameters["slow_ma"]
            trend_ma = self.parameters["trend_ma"]

            df["fast_ma"] = df["close"].rolling(window=fast_ma).mean()
            df["slow_ma"] = df["close"].rolling(window=slow_ma).mean()
            df["trend_ma"] = df["close"].rolling(window=trend_ma).mean()

            # Need enough data
            if len(df) < slow_ma + 1:
                continue

            current = df.iloc[-1]
            prev = df.iloc[-2]

            # Golden cross (buy signal)
            if (
                prev["fast_ma"] <= prev["slow_ma"]
                and current["fast_ma"] > current["slow_ma"]
                and current["close"] > current["trend_ma"]  # Trend filter
            ):
                signals.append(
                    Signal(
                        symbol=symbol,
                        action="buy",
                        quantity=self._calculate_position_size(current["close"]),
                        reason=f"Golden cross: {fast_ma}MA crossed above {slow_ma}MA, price above {trend_ma}MA trend filter",
                        metadata={
                            "fast_ma": current["fast_ma"],
                            "slow_ma": current["slow_ma"],
                            "entry_price": current["close"],
                        },
                    )
                )

            # Death cross (sell signal)
            elif (
                prev["fast_ma"] >= prev["slow_ma"]
                and current["fast_ma"] < current["slow_ma"]
            ):
                signals.append(
                    Signal(
                        symbol=symbol,
                        action="sell",
                        quantity=0,  # Sell all
                        reason=f"Death cross: {fast_ma}MA crossed below {slow_ma}MA",
                        metadata={
                            "fast_ma": current["fast_ma"],
                            "slow_ma": current["slow_ma"],
                        },
                    )
                )

        return signals

    def _calculate_position_size(self, price: float) -> float:
        """Calculate position size based on parameters"""
        # Placeholder: assumes $100,000 portfolio
        portfolio_value = 100000
        allocation = portfolio_value * (self.parameters["position_size_pct"] / 100)
        quantity = int(allocation / price)
        return max(1, quantity)

    def validate_parameters(self) -> bool:
        """Validate strategy parameters"""
        required = ["fast_ma", "slow_ma", "trend_ma", "position_size_pct"]

        for param in required:
            if param not in self.parameters:
                return False

        # Fast MA must be less than slow MA
        if self.parameters["fast_ma"] >= self.parameters["slow_ma"]:
            return False

        # Reasonable ranges
        if (
            self.parameters["fast_ma"] < 5
            or self.parameters["fast_ma"] > 200
            or self.parameters["slow_ma"] < 50
            or self.parameters["slow_ma"] > 500
        ):
            return False

        return True
