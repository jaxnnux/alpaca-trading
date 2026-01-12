"""Abstract broker interface"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime


class BrokerInterface(ABC):
    """
    Abstract base class for broker implementations

    This defines the interface that all broker implementations must follow,
    allowing AlpacaDesk to support multiple brokers in the future.
    """

    @abstractmethod
    def authenticate(self, api_key: str, secret_key: str, paper: bool = True) -> bool:
        """
        Authenticate with the broker

        Args:
            api_key: API key or username
            secret_key: Secret key or password
            paper: Whether to use paper trading (default: True)

        Returns:
            bool: True if authentication successful
        """
        pass

    @abstractmethod
    def get_account(self) -> Dict[str, Any]:
        """
        Get account information

        Returns:
            Dict containing account details
        """
        pass

    @abstractmethod
    def get_positions(self) -> List[Dict[str, Any]]:
        """
        Get all current positions

        Returns:
            List of position dictionaries
        """
        pass

    @abstractmethod
    def submit_order(
        self,
        symbol: str,
        qty: float,
        side: str,
        order_type: str,
        time_in_force: str = "day",
        limit_price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Submit an order

        Args:
            symbol: Stock symbol
            qty: Quantity to buy/sell
            side: 'buy' or 'sell'
            order_type: 'market', 'limit', 'stop', 'stop_limit'
            time_in_force: 'day', 'gtc', 'ioc', 'fok'
            limit_price: Limit price for limit orders

        Returns:
            Dict containing order details
        """
        pass

    @abstractmethod
    def get_orders(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get orders

        Args:
            status: Filter by status ('open', 'closed', 'all')

        Returns:
            List of order dictionaries
        """
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order

        Args:
            order_id: ID of the order to cancel

        Returns:
            bool: True if cancellation successful
        """
        pass

    @abstractmethod
    def get_bars(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> List[Dict[str, Any]]:
        """
        Get historical price bars

        Args:
            symbol: Stock symbol
            timeframe: Bar timeframe (e.g., '1Min', '1Hour', '1Day')
            start: Start datetime
            end: End datetime

        Returns:
            List of bar dictionaries with OHLCV data
        """
        pass

    @abstractmethod
    def subscribe_quotes(self, symbols: List[str], callback):
        """
        Subscribe to real-time quotes via WebSocket

        Args:
            symbols: List of symbols to subscribe to
            callback: Function to call when quotes are received
        """
        pass

    @abstractmethod
    def unsubscribe_quotes(self, symbols: List[str]):
        """
        Unsubscribe from real-time quotes

        Args:
            symbols: List of symbols to unsubscribe from
        """
        pass
