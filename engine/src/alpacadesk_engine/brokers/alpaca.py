"""Alpaca broker implementation"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from .interface import BrokerInterface


class AlpacaBroker(BrokerInterface):
    """
    Alpaca Markets broker implementation
    """

    def __init__(self):
        self.trading_client: Optional[TradingClient] = None
        self.data_client: Optional[StockHistoricalDataClient] = None
        self.is_paper = True

    def authenticate(self, api_key: str, secret_key: str, paper: bool = True) -> bool:
        """Authenticate with Alpaca"""
        try:
            self.is_paper = paper

            # Create trading client
            self.trading_client = TradingClient(
                api_key=api_key,
                secret_key=secret_key,
                paper=paper,
            )

            # Create data client
            self.data_client = StockHistoricalDataClient(
                api_key=api_key,
                secret_key=secret_key,
            )

            # Test connection
            self.trading_client.get_account()

            return True

        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def get_account(self) -> Dict[str, Any]:
        """Get account information"""
        if not self.trading_client:
            raise Exception("Not authenticated")

        account = self.trading_client.get_account()

        return {
            "account_number": account.account_number,
            "portfolio_value": float(account.portfolio_value),
            "buying_power": float(account.buying_power),
            "cash": float(account.cash),
            "equity": float(account.equity),
            "status": account.status.value,
            "pattern_day_trader": account.pattern_day_trader,
        }

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all current positions"""
        if not self.trading_client:
            raise Exception("Not authenticated")

        positions = self.trading_client.get_all_positions()

        return [
            {
                "symbol": pos.symbol,
                "qty": float(pos.qty),
                "avg_entry_price": float(pos.avg_entry_price),
                "current_price": float(pos.current_price),
                "market_value": float(pos.market_value),
                "cost_basis": float(pos.cost_basis),
                "unrealized_pl": float(pos.unrealized_pl),
                "unrealized_plpc": float(pos.unrealized_plpc),
                "side": pos.side.value,
            }
            for pos in positions
        ]

    def submit_order(
        self,
        symbol: str,
        qty: float,
        side: str,
        order_type: str,
        time_in_force: str = "day",
        limit_price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Submit an order"""
        if not self.trading_client:
            raise Exception("Not authenticated")

        # Convert side
        order_side = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL

        # Convert time in force
        tif_map = {
            "day": TimeInForce.DAY,
            "gtc": TimeInForce.GTC,
            "ioc": TimeInForce.IOC,
            "fok": TimeInForce.FOK,
        }
        tif = tif_map.get(time_in_force.lower(), TimeInForce.DAY)

        # Create order request
        if order_type.lower() == "market":
            order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=tif,
            )
        elif order_type.lower() == "limit":
            if limit_price is None:
                raise ValueError("Limit price required for limit orders")

            order_data = LimitOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=tif,
                limit_price=limit_price,
            )
        else:
            raise ValueError(f"Unsupported order type: {order_type}")

        # Submit order
        order = self.trading_client.submit_order(order_data)

        return {
            "id": str(order.id),
            "symbol": order.symbol,
            "qty": float(order.qty),
            "side": order.side.value,
            "type": order.type.value,
            "status": order.status.value,
        }

    def get_orders(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get orders"""
        if not self.trading_client:
            raise Exception("Not authenticated")

        # Map status
        status_map = {
            "open": QueryOrderStatus.OPEN,
            "closed": QueryOrderStatus.CLOSED,
            "all": QueryOrderStatus.ALL,
        }

        order_filter = status_map.get(status.lower() if status else "open", QueryOrderStatus.OPEN)
        orders = self.trading_client.get_orders(filter=order_filter)

        return [
            {
                "id": str(order.id),
                "symbol": order.symbol,
                "qty": float(order.qty),
                "filled_qty": float(order.filled_qty or 0),
                "side": order.side.value,
                "type": order.type.value,
                "status": order.status.value,
                "created_at": order.created_at.isoformat() if order.created_at else None,
                "filled_avg_price": float(order.filled_avg_price) if order.filled_avg_price else None,
            }
            for order in orders
        ]

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if not self.trading_client:
            raise Exception("Not authenticated")

        try:
            self.trading_client.cancel_order_by_id(order_id)
            return True
        except Exception as e:
            print(f"Failed to cancel order: {e}")
            return False

    def get_bars(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> List[Dict[str, Any]]:
        """Get historical price bars"""
        if not self.data_client:
            raise Exception("Not authenticated")

        # Map timeframe string to TimeFrame
        timeframe_map = {
            "1min": TimeFrame.Minute,
            "5min": TimeFrame(5, "Min"),
            "15min": TimeFrame(15, "Min"),
            "1hour": TimeFrame.Hour,
            "1day": TimeFrame.Day,
        }

        tf = timeframe_map.get(timeframe.lower(), TimeFrame.Day)

        # Request bars
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=tf,
            start=start,
            end=end,
        )

        bars = self.data_client.get_stock_bars(request)

        # Convert to list of dicts
        result = []
        if symbol in bars.data:
            for bar in bars.data[symbol]:
                result.append({
                    "timestamp": bar.timestamp.isoformat(),
                    "open": float(bar.open),
                    "high": float(bar.high),
                    "low": float(bar.low),
                    "close": float(bar.close),
                    "volume": int(bar.volume),
                })

        return result

    def subscribe_quotes(self, symbols: List[str], callback):
        """Subscribe to real-time quotes via WebSocket"""
        # TODO: Implement WebSocket subscription
        # This would use alpaca.data.live.StockDataStream
        pass

    def unsubscribe_quotes(self, symbols: List[str]):
        """Unsubscribe from real-time quotes"""
        # TODO: Implement WebSocket unsubscription
        pass
