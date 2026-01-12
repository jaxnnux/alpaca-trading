"""Mean Reversion RSI Strategy"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np

from .base import BaseStrategy, Signal


class MeanReversionRSIStrategy(BaseStrategy):
    """
    Mean Reversion RSI Strategy

    Buy when RSI is oversold and price is above 200MA.
    Sell when RSI is overbought.

    Parameters:
    - rsi_period: RSI calculation period (default: 14)
    - rsi_oversold: Oversold threshold (default: 30)
    - rsi_overbought: Overbought threshold (default: 70)
    - ma_period: Moving average period for trend filter (default: 200)
    - position_size_pct: Percentage of portfolio to allocate (default: 10)
    """

    def __init__(self, symbols: List[str], parameters: Dict[str, Any]):
        default_params = {
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70,
            "ma_period": 200,
            "position_size_pct": 10,
        }
        default_params.update(parameters)

        super().__init__(
            name="Mean Reversion RSI",
            symbols=symbols,
            parameters=default_params,
        )

    def analyze(self, market_data: Dict[str, pd.DataFrame]) -> List[Signal]:
        """
        Generate trading signals based on RSI mean reversion logic
        """
        signals = []

        for symbol in self.symbols:
            if symbol not in market_data or market_data[symbol].empty:
                continue

            df = market_data[symbol].copy()

            # Calculate RSI
            df["rsi"] = self._calculate_rsi(df["close"], self.parameters["rsi_period"])

            # Calculate moving average
            df["ma"] = df["close"].rolling(window=self.parameters["ma_period"]).mean()

            # Current conditions
            if len(df) < self.parameters["ma_period"]:
                continue

            current = df.iloc[-1]

            # Buy signal: RSI oversold + price above MA
            if (
                current["rsi"] < self.parameters["rsi_oversold"]
                and current["close"] > current["ma"]
            ):
                signals.append(
                    Signal(
                        symbol=symbol,
                        action="buy",
                        quantity=self._calculate_position_size(current["close"]),
                        reason=f"RSI oversold: {current['rsi']:.1f} < {self.parameters['rsi_oversold']}, price above {self.parameters['ma_period']}MA",
                        metadata={
                            "rsi": current["rsi"],
                            "ma": current["ma"],
                            "entry_price": current["close"],
                        },
                    )
                )

            # Sell signal: RSI overbought (for existing positions)
            elif current["rsi"] > self.parameters["rsi_overbought"]:
                signals.append(
                    Signal(
                        symbol=symbol,
                        action="sell",
                        quantity=0,  # Sell all
                        reason=f"RSI overbought: {current['rsi']:.1f} > {self.parameters['rsi_overbought']}",
                        metadata={
                            "rsi": current["rsi"],
                        },
                    )
                )

        return signals

    def _calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Relative Strength Index
        """
        delta = prices.diff()

        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def _calculate_position_size(self, price: float) -> float:
        """Calculate position size based on parameters"""
        # Placeholder: assumes $100,000 portfolio
        portfolio_value = 100000
        allocation = portfolio_value * (self.parameters["position_size_pct"] / 100)
        quantity = int(allocation / price)
        return max(1, quantity)

    def validate_parameters(self) -> bool:
        """Validate strategy parameters"""
        required = [
            "rsi_period",
            "rsi_oversold",
            "rsi_overbought",
            "ma_period",
            "position_size_pct",
        ]

        for param in required:
            if param not in self.parameters:
                return False

        # Validate ranges
        if self.parameters["rsi_period"] < 5 or self.parameters["rsi_period"] > 50:
            return False

        if (
            self.parameters["rsi_oversold"] < 10
            or self.parameters["rsi_oversold"] > 40
        ):
            return False

        if (
            self.parameters["rsi_overbought"] < 60
            or self.parameters["rsi_overbought"] > 90
        ):
            return False

        if self.parameters["ma_period"] < 50 or self.parameters["ma_period"] > 300:
            return False

        return True
