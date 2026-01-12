"""Strategy management API endpoints with database persistence"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import uuid

from ..utils.database import get_db_session
from ..utils.models import Strategy as StrategyModel

router = APIRouter()


class StrategyConfig(BaseModel):
    name: str
    type: str
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
    """Create a new strategy and persist to database"""
    try:
        with get_db() as db:
            strategy_id = str(uuid.uuid4())

            db_strategy = StrategyModel(
                id=strategy_id,
                name=strategy.name,
                type=strategy.type,
                enabled=strategy.enabled,
            )

            # Set symbols and parameters using helper methods
            db_strategy.set_symbols_list(strategy.symbols)
            db_strategy.set_parameters_dict(strategy.parameters)

            db.add(db_strategy)
            db.commit()
            db.refresh(db_strategy)

            return {
                "success": True,
                "strategy": {
                    "id": db_strategy.id,
                    "name": db_strategy.name,
                    "type": db_strategy.type,
                    "symbols": db_strategy.get_symbols_list(),
                    "parameters": db_strategy.get_parameters_dict(),
                    "enabled": db_strategy.enabled,
                    "created_at": db_strategy.created_at.isoformat(),
                }
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create strategy: {str(e)}")


@router.get("/list")
async def list_strategies():
    """List all strategies from database"""
    try:
        with get_db() as db:
            strategies = db.query(StrategyModel).all()

            strategy_list = []
            for s in strategies:
                strategy_list.append({
                    "id": s.id,
                    "name": s.name,
                    "type": s.type,
                    "symbols": s.get_symbols_list(),
                    "parameters": s.get_parameters_dict(),
                    "enabled": s.enabled,
                    "created_at": s.created_at.isoformat(),
                })

            return {"strategies": strategy_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list strategies: {str(e)}")


@router.get("/{strategy_id}")
async def get_strategy(strategy_id: str):
    """Get a specific strategy"""
    try:
        with get_db() as db:
            strategy = db.query(StrategyModel).filter(StrategyModel.id == strategy_id).first()

            if not strategy:
                raise HTTPException(status_code=404, detail="Strategy not found")

            return {
                "strategy": {
                    "id": strategy.id,
                    "name": strategy.name,
                    "type": strategy.type,
                    "symbols": strategy.get_symbols_list(),
                    "parameters": strategy.get_parameters_dict(),
                    "enabled": strategy.enabled,
                    "created_at": strategy.created_at.isoformat(),
                }
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get strategy: {str(e)}")


@router.put("/{strategy_id}")
async def update_strategy(strategy_id: str, strategy: StrategyConfig):
    """Update an existing strategy"""
    try:
        with get_db() as db:
            db_strategy = db.query(StrategyModel).filter(StrategyModel.id == strategy_id).first()

            if not db_strategy:
                raise HTTPException(status_code=404, detail="Strategy not found")

            # Update fields
            db_strategy.name = strategy.name
            db_strategy.type = strategy.type
            db_strategy.enabled = strategy.enabled
            db_strategy.set_symbols_list(strategy.symbols)
            db_strategy.set_parameters_dict(strategy.parameters)

            db.commit()
            db.refresh(db_strategy)

            return {
                "success": True,
                "strategy": {
                    "id": db_strategy.id,
                    "name": db_strategy.name,
                    "type": db_strategy.type,
                    "symbols": db_strategy.get_symbols_list(),
                    "parameters": db_strategy.get_parameters_dict(),
                    "enabled": db_strategy.enabled,
                    "created_at": db_strategy.created_at.isoformat(),
                }
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update strategy: {str(e)}")


@router.delete("/{strategy_id}")
async def delete_strategy(strategy_id: str):
    """Delete a strategy"""
    try:
        with get_db() as db:
            strategy = db.query(StrategyModel).filter(StrategyModel.id == strategy_id).first()

            if not strategy:
                raise HTTPException(status_code=404, detail="Strategy not found")

            db.delete(strategy)
            db.commit()

            return {"success": True, "message": f"Strategy {strategy_id} deleted"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete strategy: {str(e)}")


@router.post("/{strategy_id}/toggle")
async def toggle_strategy(strategy_id: str):
    """Enable/disable a strategy"""
    try:
        with get_db() as db:
            strategy = db.query(StrategyModel).filter(StrategyModel.id == strategy_id).first()

            if not strategy:
                raise HTTPException(status_code=404, detail="Strategy not found")

            strategy.enabled = not strategy.enabled
            db.commit()
            db.refresh(strategy)

            return {
                "success": True,
                "enabled": strategy.enabled,
                "strategy": {
                    "id": strategy.id,
                    "name": strategy.name,
                    "type": strategy.type,
                    "symbols": strategy.get_symbols_list(),
                    "parameters": strategy.get_parameters_dict(),
                    "enabled": strategy.enabled,
                    "created_at": strategy.created_at.isoformat(),
                }
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to toggle strategy: {str(e)}")


@router.get("/templates/list")
async def list_strategy_templates():
    """Get list of pre-built strategy templates"""
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
