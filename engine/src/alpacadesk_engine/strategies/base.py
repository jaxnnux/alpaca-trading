"""Base strategy class"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd


class Signal:
    """Trading signal"""

    def __init__(
        self,
        symbol: str,
        action: str,  # 'buy', 'sell', 'hold'
        quantity: float,
        reason: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.symbol = symbol
        self.action = action
        self.quantity = quantity
        self.reason = reason
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies

    All strategies must implement:
    - analyze(): Generate trading signals based on market data
    - get_parameters(): Return strategy parameters
    - set_parameters(): Update strategy parameters
    """

    def __init__(self, name: str, symbols: List[str], parameters: Dict[str, Any]):
        self.name = name
        self.symbols = symbols
        self.parameters = parameters
        self.enabled = False

    @abstractmethod
    def analyze(
        self,
        market_data: Dict[str, pd.DataFrame],
        portfolio_value: Optional[float] = None
    ) -> List[Signal]:
        """
        Analyze market data and generate trading signals

        Args:
            market_data: Dictionary mapping symbols to DataFrame with OHLCV data
            portfolio_value: Current portfolio value for position sizing (optional)

        Returns:
            List of Signal objects
        """
        pass

    def _calculate_position_size(
        self,
        price: float,
        portfolio_value: Optional[float] = None,
        position_size_pct: Optional[float] = None
    ) -> float:
        """
        Calculate position size based on portfolio value and percentage

        Args:
            price: Current price of the asset
            portfolio_value: Current portfolio value (required)
            position_size_pct: Percentage of portfolio to allocate (uses strategy default if not provided)

        Returns:
            Number of shares to buy

        Raises:
            ValueError: If portfolio_value is not provided
        """
        if portfolio_value is None or portfolio_value <= 0:
            raise ValueError("Portfolio value must be provided and greater than 0")

        if position_size_pct is None:
            position_size_pct = self.parameters.get("position_size_pct", 10)

        # Validate position size percentage
        if position_size_pct <= 0 or position_size_pct > 100:
            raise ValueError(f"Position size percentage must be between 0 and 100, got {position_size_pct}")

        allocation = portfolio_value * (position_size_pct / 100)
        quantity = int(allocation / price)

        # Ensure at least 1 share if allocation allows
        return max(1, quantity) if allocation >= price else 0

    def get_parameters(self) -> Dict[str, Any]:
        """Get current strategy parameters"""
        return self.parameters.copy()

    def set_parameters(self, parameters: Dict[str, Any]):
        """Update strategy parameters"""
        self.parameters.update(parameters)

    def enable(self):
        """Enable the strategy"""
        self.enabled = True

    def disable(self):
        """Disable the strategy"""
        self.enabled = False

    def is_enabled(self) -> bool:
        """Check if strategy is enabled"""
        return self.enabled

    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters

        Returns:
            bool: True if parameters are valid
        """
        # Override in subclasses for custom validation
        return True

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, symbols={self.symbols}, enabled={self.enabled})"
