"""System and monitoring API endpoints"""

from fastapi import APIRouter
from ..utils.rate_limiter import rate_limiter

router = APIRouter()


@router.get("/rate-limits")
async def get_rate_limits():
    """
    Get current rate limit status for all endpoints
    """
    return rate_limiter.get_status()


@router.get("/health-detailed")
async def get_detailed_health():
    """
    Get detailed system health information
    """
    import psutil
    import platform

    return {
        "status": "healthy",
        "system": {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
        },
        "rate_limits": rate_limiter.get_status(),
    }
