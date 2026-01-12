"""Momentum Breakout Strategy"""

from typing import List, Dict, Any
import pandas as pd
import numpy as np

from .base import BaseStrategy, Signal


class MomentumBreakoutStrategy(BaseStrategy):
    """
    Momentum Breakout Strategy

    Buy when price exceeds N-day high with volume confirmation.

    Parameters:
    - lookback_period: Number of days to look back for highs (default: 20)
    - volume_multiplier: Volume must be X times average volume (default: 1.5)
    - position_size_pct: Percentage of portfolio to allocate (default: 10)
    - stop_loss_pct: Stop loss percentage below entry (default: 5)
    - take_profit_pct: Take profit percentage above entry (default: 15)
    - max_positions: Maximum concurrent positions (default: 5)
    """

    def __init__(self, symbols: List[str], parameters: Dict[str, Any]):
        default_params = {
            "lookback_period": 20,
            "volume_multiplier": 1.5,
            "position_size_pct": 10,
            "stop_loss_pct": 5,
            "take_profit_pct": 15,
            "max_positions": 5,
        }
        default_params.update(parameters)

        super().__init__(
            name="Momentum Breakout",
            symbols=symbols,
            parameters=default_params,
        )

    def analyze(self, market_data: Dict[str, pd.DataFrame]) -> List[Signal]:
        """
        Generate trading signals based on momentum breakout logic
        """
        signals = []

        for symbol in self.symbols:
            if symbol not in market_data or market_data[symbol].empty:
                continue

            df = market_data[symbol].copy()

            # Calculate indicators
            lookback = self.parameters["lookback_period"]

            # N-day high
            df["high_n"] = df["high"].rolling(window=lookback).max()

            # Average volume
            df["avg_volume"] = df["volume"].rolling(window=lookback).mean()

            # Current conditions
            if len(df) < lookback + 1:
                continue

            current = df.iloc[-1]
            prev = df.iloc[-2]

            # Breakout condition: price breaks above N-day high
            breakout = (
                current["close"] > prev["high_n"]
                and current["volume"] > self.parameters["volume_multiplier"] * current["avg_volume"]
            )

            if breakout:
                signals.append(
                    Signal(
                        symbol=symbol,
                        action="buy",
                        quantity=self._calculate_position_size(current["close"]),
                        reason=f"Momentum breakout: price {current['close']:.2f} > {lookback}d high {prev['high_n']:.2f}",
                        metadata={
                            "entry_price": current["close"],
                            "stop_loss": current["close"] * (1 - self.parameters["stop_loss_pct"] / 100),
                            "take_profit": current["close"] * (1 + self.parameters["take_profit_pct"] / 100),
                        },
                    )
                )

        return signals

    def _calculate_position_size(self, price: float) -> float:
        """
        Calculate position size based on parameters

        Note: In production, this would access portfolio value.
        For now, returns a placeholder quantity.
        """
        # Placeholder: assumes $100,000 portfolio
        portfolio_value = 100000
        allocation = portfolio_value * (self.parameters["position_size_pct"] / 100)
        quantity = int(allocation / price)
        return max(1, quantity)

    def validate_parameters(self) -> bool:
        """Validate strategy parameters"""
        required = [
            "lookback_period",
            "volume_multiplier",
            "position_size_pct",
            "stop_loss_pct",
            "take_profit_pct",
            "max_positions",
        ]

        for param in required:
            if param not in self.parameters:
                return False

        # Validate ranges
        if self.parameters["lookback_period"] < 5 or self.parameters["lookback_period"] > 100:
            return False

        if self.parameters["volume_multiplier"] < 1.0 or self.parameters["volume_multiplier"] > 5.0:
            return False

        if self.parameters["position_size_pct"] < 1 or self.parameters["position_size_pct"] > 50:
            return False

        return True
