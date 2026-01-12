"""FastAPI main application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api import auth, account, orders, strategies, backtest


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    print("🚀 AlpacaDesk Engine starting...")
    yield
    # Shutdown
    print("👋 AlpacaDesk Engine shutting down...")


app = FastAPI(
    title="AlpacaDesk Engine",
    description="Trading engine backend for AlpacaDesk",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware for Electron app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(account.router, prefix="/api/account", tags=["account"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(strategies.router, prefix="/api/strategies", tags=["strategies"])
app.include_router(backtest.router, prefix="/api/backtest", tags=["backtest"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "alpacadesk-engine"}


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "services": {
            "api": "operational",
        }
    }
