"""Strategy management API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

router = APIRouter()

# In-memory strategy storage (would use database in production)
_strategies = {}


class StrategyConfig(BaseModel):
    name: str
    type: str  # momentum, mean_reversion, dual_ma, etc.
    symbols: List[str]
    parameters: Dict[str, Any]
    enabled: bool = False


class StrategyResponse(BaseModel):
    id: str
    name: str
    type: str
    symbols: List[str]
    parameters: Dict[str, Any]
    enabled: bool
    created_at: str


@router.post("/create")
async def create_strategy(strategy: StrategyConfig):
    """
    Create a new strategy
    """
    try:
        import uuid
        from datetime import datetime

        strategy_id = str(uuid.uuid4())

        strategy_data = {
            "id": strategy_id,
            "name": strategy.name,
            "type": strategy.type,
            "symbols": strategy.symbols,
            "parameters": strategy.parameters,
            "enabled": strategy.enabled,
            "created_at": datetime.utcnow().isoformat(),
        }

        _strategies[strategy_id] = strategy_data

        return {"success": True, "strategy": strategy_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create strategy: {str(e)}")


@router.get("/list")
async def list_strategies():
    """
    List all strategies
    """
    return {"strategies": list(_strategies.values())}


@router.get("/{strategy_id}")
async def get_strategy(strategy_id: str):
    """
    Get a specific strategy
    """
    if strategy_id not in _strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")

    return {"strategy": _strategies[strategy_id]}


@router.put("/{strategy_id}")
async def update_strategy(strategy_id: str, strategy: StrategyConfig):
    """
    Update an existing strategy
    """
    if strategy_id not in _strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")

    try:
        _strategies[strategy_id].update({
            "name": strategy.name,
            "type": strategy.type,
            "symbols": strategy.symbols,
            "parameters": strategy.parameters,
            "enabled": strategy.enabled,
        })

        return {"success": True, "strategy": _strategies[strategy_id]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update strategy: {str(e)}")


@router.delete("/{strategy_id}")
async def delete_strategy(strategy_id: str):
    """
    Delete a strategy
    """
    if strategy_id not in _strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")

    del _strategies[strategy_id]
    return {"success": True, "message": f"Strategy {strategy_id} deleted"}


@router.post("/{strategy_id}/toggle")
async def toggle_strategy(strategy_id: str):
    """
    Enable/disable a strategy
    """
    if strategy_id not in _strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")

    try:
        _strategies[strategy_id]["enabled"] = not _strategies[strategy_id]["enabled"]

        return {
            "success": True,
            "enabled": _strategies[strategy_id]["enabled"],
            "strategy": _strategies[strategy_id]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle strategy: {str(e)}")


@router.get("/templates/list")
async def list_strategy_templates():
    """
    Get list of pre-built strategy templates
    """
    templates = [
        {
            "id": "momentum_breakout",
            "name": "Momentum Breakout",
            "description": "Buy when price exceeds N-day high with volume confirmation",
            "default_parameters": {
                "lookback_period": 20,
                "volume_multiplier": 1.5,
                "position_size_pct": 10,
                "stop_loss_pct": 5,
                "take_profit_pct": 15,
                "max_positions": 5,
            },
            "typical_trades_per_month": "5-15",
        },
        {
            "id": "mean_reversion_rsi",
            "name": "Mean Reversion RSI",
            "description": "Buy when RSI oversold + price above 200MA; sell when RSI overbought",
            "default_parameters": {
                "rsi_period": 14,
                "rsi_oversold": 30,
                "rsi_overbought": 70,
                "ma_period": 200,
                "position_size_pct": 10,
            },
            "typical_trades_per_month": "10-25",
        },
        {
            "id": "dual_moving_average",
            "name": "Dual Moving Average",
            "description": "Classic golden/death cross with trend filter",
            "default_parameters": {
                "fast_ma": 50,
                "slow_ma": 200,
                "trend_ma": 20,
                "position_size_pct": 20,
            },
            "typical_trades_per_month": "3-8",
        },
    ]

    return {"templates": templates}
