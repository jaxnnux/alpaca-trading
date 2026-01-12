"""Bollinger Band Bounce Strategy"""

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

from .base import BaseStrategy, Signal


class BollingerBandStrategy(BaseStrategy):
    """
    Bollinger Band Bounce Strategy

    Buy when price touches lower band with confirmation.
    Sell when price touches upper band.

    Parameters:
    - bb_period: Bollinger Band period (default: 20)
    - bb_std_dev: Number of standard deviations (default: 2.0)
    - confirmation_candles: Candles to confirm bounce (default: 1)
    - position_size_pct: Percentage of portfolio to allocate (default: 10)
    """

    def __init__(self, symbols: List[str], parameters: Dict[str, Any]):
        default_params = {
            "bb_period": 20,
            "bb_std_dev": 2.0,
            "confirmation_candles": 1,
            "position_size_pct": 10,
        }
        default_params.update(parameters)

        super().__init__(
            name="Bollinger Band Bounce",
            symbols=symbols,
            parameters=default_params,
        )

    def analyze(
        self,
        market_data: Dict[str, pd.DataFrame],
        portfolio_value: Optional[float] = None
    ) -> List[Signal]:
        """
        Generate trading signals based on Bollinger Band bounces
        """
        signals = []

        for symbol in self.symbols:
            if symbol not in market_data or market_data[symbol].empty:
                continue

            df = market_data[symbol].copy()

            # Calculate Bollinger Bands
            period = self.parameters["bb_period"]
            std_dev = self.parameters["bb_std_dev"]

            df["sma"] = df["close"].rolling(window=period).mean()
            df["std"] = df["close"].rolling(window=period).std()
            df["upper_band"] = df["sma"] + (df["std"] * std_dev)
            df["lower_band"] = df["sma"] - (df["std"] * std_dev)

            # Band width for volatility measure
            df["band_width"] = (df["upper_band"] - df["lower_band"]) / df["sma"]

            # Need enough data
            if len(df) < period + 2:
                continue

            current = df.iloc[-1]
            prev = df.iloc[-2]

            # Buy signal: bounce off lower band
            if (
                prev["close"] <= prev["lower_band"]
                and current["close"] > current["lower_band"]
                and current["close"] < current["sma"]  # Still below middle
            ):
                try:
                    quantity = self._calculate_position_size(current["close"], portfolio_value)
                    signals.append(
                        Signal(
                            symbol=symbol,
                            action="buy",
                            quantity=quantity,
                            reason=f"Bollinger bounce: price bounced off lower band at {current['lower_band']:.2f}",
                            metadata={
                                "entry_price": current["close"],
                                "lower_band": current["lower_band"],
                                "upper_band": current["upper_band"],
                                "sma": current["sma"],
                            },
                        )
                    )
                except ValueError as e:
                    print(f"Skipping signal for {symbol}: {e}")
                    continue

            # Sell signal: touch upper band
            elif (
                current["close"] >= current["upper_band"]
                or (prev["close"] < prev["sma"] and current["close"] >= current["sma"])
            ):
                signals.append(
                    Signal(
                        symbol=symbol,
                        action="sell",
                        quantity=0,  # Sell all
                        reason=f"Bollinger exit: price reached upper band or crossed SMA",
                        metadata={
                            "exit_price": current["close"],
                            "upper_band": current["upper_band"],
                        },
                    )
                )

        return signals

    def validate_parameters(self) -> bool:
        """Validate strategy parameters"""
        required = ["bb_period", "bb_std_dev", "confirmation_candles", "position_size_pct"]

        for param in required:
            if param not in self.parameters:
                return False

        # Reasonable ranges
        if (
            self.parameters["bb_period"] < 10
            or self.parameters["bb_period"] > 100
            or self.parameters["bb_std_dev"] < 1.0
            or self.parameters["bb_std_dev"] > 3.0
        ):
            return False

        return True
