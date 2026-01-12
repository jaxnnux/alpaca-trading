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
    def analyze(self, market_data: Dict[str, pd.DataFrame]) -> List[Signal]:
        """
        Analyze market data and generate trading signals

        Args:
            market_data: Dictionary mapping symbols to DataFrame with OHLCV data

        Returns:
            List of Signal objects
        """
        pass

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
