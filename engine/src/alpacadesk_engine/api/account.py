"""Account API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from .auth import get_current_client

router = APIRouter()


class AccountInfo(BaseModel):
    account_number: str
    portfolio_value: float
    buying_power: float
    cash: float
    equity: float
    status: str
    pattern_day_trader: bool


@router.get("/info", response_model=AccountInfo)
async def get_account_info():
    """
    Get account information
    """
    try:
        client = get_current_client()
        account = client.get_account()

        return AccountInfo(
            account_number=account.account_number,
            portfolio_value=float(account.portfolio_value),
            buying_power=float(account.buying_power),
            cash=float(account.cash),
            equity=float(account.equity),
            status=account.status.value,
            pattern_day_trader=account.pattern_day_trader,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get account info: {str(e)}")


@router.get("/positions")
async def get_positions():
    """
    Get all current positions
    """
    try:
        client = get_current_client()
        positions = client.get_all_positions()

        return {
            "positions": [
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
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get positions: {str(e)}")


@router.get("/history")
async def get_account_history():
    """
    Get account portfolio history
    """
    try:
        client = get_current_client()
        history = client.get_portfolio_history(period="1M", timeframe="1D")

        return {
            "timestamp": history.timestamp,
            "equity": history.equity,
            "profit_loss": history.profit_loss,
            "profit_loss_pct": history.profit_loss_pct,
            "base_value": float(history.base_value),
            "timeframe": history.timeframe.value,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get account history: {str(e)}")
