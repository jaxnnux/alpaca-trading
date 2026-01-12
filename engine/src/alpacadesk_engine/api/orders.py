"""Orders API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Literal
from decimal import Decimal

from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from .auth import get_current_client

router = APIRouter()


class OrderRequest(BaseModel):
    symbol: str
    qty: float
    side: Literal["buy", "sell"]
    type: Literal["market", "limit"]
    time_in_force: Literal["day", "gtc", "ioc"] = "day"
    limit_price: Optional[float] = None


@router.post("/submit")
async def submit_order(order: OrderRequest):
    """
    Submit a new order
    """
    try:
        client = get_current_client()

        # Convert side
        side = OrderSide.BUY if order.side == "buy" else OrderSide.SELL

        # Convert time in force
        tif_map = {
            "day": TimeInForce.DAY,
            "gtc": TimeInForce.GTC,
            "ioc": TimeInForce.IOC,
        }
        time_in_force = tif_map[order.time_in_force]

        # Create order request
        if order.type == "market":
            order_data = MarketOrderRequest(
                symbol=order.symbol,
                qty=order.qty,
                side=side,
                time_in_force=time_in_force,
            )
        elif order.type == "limit":
            if order.limit_price is None:
                raise HTTPException(status_code=400, detail="Limit price required for limit orders")

            order_data = LimitOrderRequest(
                symbol=order.symbol,
                qty=order.qty,
                side=side,
                time_in_force=time_in_force,
                limit_price=order.limit_price,
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported order type: {order.type}")

        # Submit order
        submitted_order = client.submit_order(order_data)

        return {
            "success": True,
            "order_id": submitted_order.id,
            "symbol": submitted_order.symbol,
            "status": submitted_order.status.value,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit order: {str(e)}")


@router.get("/list")
async def list_orders(status: Optional[str] = None):
    """
    List orders
    """
    try:
        client = get_current_client()

        # Get orders
        if status:
            from alpaca.trading.enums import QueryOrderStatus
            status_map = {
                "open": QueryOrderStatus.OPEN,
                "closed": QueryOrderStatus.CLOSED,
                "all": QueryOrderStatus.ALL,
            }
            order_status = status_map.get(status, QueryOrderStatus.OPEN)
            orders = client.get_orders(filter=order_status)
        else:
            orders = client.get_orders()

        return {
            "orders": [
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
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list orders: {str(e)}")


@router.delete("/{order_id}")
async def cancel_order(order_id: str):
    """
    Cancel an order
    """
    try:
        client = get_current_client()
        client.cancel_order_by_id(order_id)

        return {"success": True, "message": f"Order {order_id} cancelled"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel order: {str(e)}")


@router.delete("/all")
async def cancel_all_orders():
    """
    Cancel all open orders
    """
    try:
        client = get_current_client()
        cancelled = client.cancel_orders()

        return {
            "success": True,
            "message": f"Cancelled {len(cancelled)} orders",
            "cancelled_ids": [str(order.id) for order in cancelled],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel all orders: {str(e)}")
