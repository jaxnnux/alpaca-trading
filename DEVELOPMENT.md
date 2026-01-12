# AlpacaDesk Development Guide

## Project Structure

This project follows a hybrid architecture with an Electron frontend (React + TypeScript) and a Python backend (FastAPI).

### Directory Layout

```
alpacadesk/
├── electron/                   # Electron main process
│   ├── main.ts                # App lifecycle, Python bridge
│   └── preload.ts             # IPC bridge
│
├── src/                        # React frontend
│   ├── components/            # UI components
│   │   ├── common/           # Shared components
│   │   ├── dashboard/        # Dashboard views
│   │   ├── strategies/       # Strategy management
│   │   ├── builder/          # Visual strategy builder
│   │   ├── backtest/         # Backtesting UI
│   │   └── settings/         # Settings pages
│   ├── hooks/                # Custom React hooks
│   ├── services/             # API service layer
│   ├── store/                # Zustand state management
│   └── types/                # TypeScript type definitions
│
├── engine/                     # Python trading engine
│   └── src/alpacadesk_engine/
│       ├── main.py           # FastAPI entry point
│       ├── api/              # HTTP API routes
│       │   ├── auth.py       # Authentication
│       │   ├── account.py    # Account management
│       │   ├── orders.py     # Order execution
│       │   ├── strategies.py # Strategy management
│       │   └── backtest.py   # Backtesting
│       ├── brokers/          # Broker implementations
│       │   ├── interface.py  # Abstract broker interface
│       │   └── alpaca.py     # Alpaca implementation
│       ├── strategies/       # Trading strategies
│       │   ├── base.py       # Base strategy class
│       │   ├── momentum.py   # Momentum strategy
│       │   └── mean_reversion.py  # Mean reversion
│       ├── backtest/         # Backtesting engine
│       ├── indicators/       # Technical indicators
│       ├── services/         # Business logic
│       └── utils/            # Utilities
│
└── resources/                 # Static assets
```

## Development Workflow

### Initial Setup

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Install Python dependencies:**
   ```bash
   cd engine
   pip install -e ".[dev]"
   cd ..
   ```

### Running in Development Mode

**Option 1: Run both services together**
```bash
npm run dev
```

**Option 2: Run separately**

Terminal 1 - Frontend:
```bash
npm run dev:electron
```

Terminal 2 - Backend:
```bash
cd engine
uvicorn src.alpacadesk_engine.main:app --reload --port 8765
```

### Architecture Overview

#### Communication Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Electron Main Process                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  - Manages Python subprocess                          │ │
│  │  - Handles window lifecycle                           │ │
│  │  - IPC communication                                  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    React Renderer                           │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Components → Services → API (http://localhost:8765)  │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST
                   ▼
┌─────────────────────────────────────────────────────────────┐
│              Python FastAPI Backend (Port 8765)             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API Routes → Brokers → Alpaca API                    │ │
│  │  └── Strategies → Market Data → Signals               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### State Management

- **Frontend State**: Zustand for React state management
- **Backend State**: In-memory session storage (will migrate to SQLite)
- **Credentials**: Windows Credential Manager via `keyring` library

#### Security

- API keys stored using Windows DPAPI (Data Protection API)
- Keys never transmitted to external servers (except Alpaca)
- All API communication happens directly from user's machine to Alpaca

## Key Components

### Authentication Flow

1. User enters Alpaca API keys in LoginPage
2. Frontend sends credentials to backend `/api/auth/login`
3. Backend validates with Alpaca API
4. If valid, stores in Windows Credential Manager
5. Creates authenticated TradingClient
6. Returns success to frontend
7. Frontend sets authenticated state, shows Dashboard

### Strategy Execution Flow

1. User selects/configures strategy
2. Strategy saved via `/api/strategies/create`
3. Strategy enabled via `/api/strategies/{id}/toggle`
4. Backend periodically evaluates strategy:
   - Fetches market data from Alpaca
   - Runs strategy `analyze()` method
   - Generates signals (buy/sell)
   - Executes orders via `/api/orders/submit`

### Backtesting Flow

1. User configures backtest parameters
2. Frontend calls `/api/backtest/run`
3. Backend:
   - Fetches historical data from Alpaca
   - Simulates strategy execution
   - Calculates performance metrics
   - Returns results (equity curve, metrics)
4. Frontend displays results in charts

## Code Style

### TypeScript/React

- Use functional components with hooks
- Prefer `const` over `let`
- Use TypeScript strict mode
- Follow React best practices (memo, useCallback for optimization)

### Python

- Follow PEP 8 style guide
- Use type hints
- Document functions with docstrings
- Use Black for formatting (100 char line length)

## Testing

### Frontend Tests

```bash
npm test
```

### Backend Tests

```bash
cd engine
pytest
```

## Building for Production

```bash
npm run build
```

This will:
1. Compile TypeScript to JavaScript
2. Bundle React app with Vite
3. Package Python backend with PyInstaller
4. Create Windows installer with Electron Builder

Output: `release/AlpacaDesk Setup.exe`

## Troubleshooting

### Python backend won't start

- Check if port 8765 is already in use
- Verify Python dependencies are installed
- Check engine/src/alpacadesk_engine/main.py for errors

### Electron app shows blank screen

- Check browser console (F12) for errors
- Verify backend is running on port 8765
- Check CORS configuration in FastAPI

### Authentication fails

- Verify Alpaca API keys are correct
- Check if using paper/live keys correctly
- Ensure Windows Credential Manager is accessible

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## Next Steps

Priority features to implement:

1. **WebSocket Integration** - Real-time market data
2. **Strategy Engine Scheduler** - Periodic strategy evaluation
3. **Visual Strategy Builder** - Drag-and-drop UI
4. **Advanced Backtesting** - Realistic slippage/fees
5. **Performance Dashboard** - Charts and metrics
6. **Multi-broker Support** - IBKR, Tradier integration

For detailed requirements, see `ALPACADESK_PRD_v1.1.md`.
