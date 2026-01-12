"""Strategy scheduler API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from ..services.scheduler import StrategyScheduler
from .auth import get_current_client

router = APIRouter()

# Global scheduler instance (would be managed better in production)
_scheduler: StrategyScheduler = None


def get_scheduler() -> StrategyScheduler:
    """Get or create scheduler instance"""
    global _scheduler
    if _scheduler is None:
        try:
            client = get_current_client()
            # Access the broker from the client
            # This is a simplified approach - production would use dependency injection
            from ..brokers.alpaca import AlpacaBroker
            broker = AlpacaBroker()
            # Re-authenticate broker (credentials should be in session)
            # For now, scheduler will work with whatever client is active
            _scheduler = StrategyScheduler(broker)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create scheduler: {str(e)}")

    return _scheduler


class SchedulerStrategyRequest(BaseModel):
    strategy_id: str
    strategy_type: str
    symbols: List[str]
    parameters: Dict[str, Any]
    interval_seconds: int = 60


@router.post("/add-strategy")
async def add_strategy(request: SchedulerStrategyRequest):
    """
    Add a strategy to the scheduler
    """
    try:
        scheduler = get_scheduler()

        scheduler.add_strategy(
            strategy_id=request.strategy_id,
            strategy_type=request.strategy_type,
            symbols=request.symbols,
            parameters=request.parameters,
            interval_seconds=request.interval_seconds,
        )

        return {"success": True, "message": f"Strategy {request.strategy_id} added"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add strategy: {str(e)}")


@router.post("/enable/{strategy_id}")
async def enable_strategy(strategy_id: str):
    """
    Enable a strategy
    """
    try:
        scheduler = get_scheduler()
        scheduler.enable_strategy(strategy_id)

        return {"success": True, "message": f"Strategy {strategy_id} enabled"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enable strategy: {str(e)}")


@router.post("/disable/{strategy_id}")
async def disable_strategy(strategy_id: str):
    """
    Disable a strategy
    """
    try:
        scheduler = get_scheduler()
        scheduler.disable_strategy(strategy_id)

        return {"success": True, "message": f"Strategy {strategy_id} disabled"}

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to disable strategy: {str(e)}")


@router.delete("/{strategy_id}")
async def remove_strategy(strategy_id: str):
    """
    Remove a strategy from the scheduler
    """
    try:
        scheduler = get_scheduler()
        scheduler.remove_strategy(strategy_id)

        return {"success": True, "message": f"Strategy {strategy_id} removed"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove strategy: {str(e)}")


@router.post("/start")
async def start_scheduler():
    """
    Start the scheduler
    """
    try:
        scheduler = get_scheduler()
        await scheduler.start()

        return {"success": True, "message": "Scheduler started"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scheduler: {str(e)}")


@router.post("/stop")
async def stop_scheduler():
    """
    Stop the scheduler
    """
    try:
        scheduler = get_scheduler()
        await scheduler.stop()

        return {"success": True, "message": "Scheduler stopped"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop scheduler: {str(e)}")


@router.get("/status")
async def get_scheduler_status():
    """
    Get scheduler status and statistics
    """
    try:
        scheduler = get_scheduler()
        return scheduler.get_status()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get scheduler status: {str(e)}")
