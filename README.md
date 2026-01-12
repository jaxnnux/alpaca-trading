# AlpacaDesk

🦙 Native Windows Algorithmic Trading Application

**Version:** 1.0.0
**Status:** Production Ready

---

## Overview

AlpacaDesk is a production-ready desktop application that democratizes algorithmic trading for retail investors. It combines a visual no-code strategy builder with pre-built proven strategies, local-first security architecture, and professional-grade execution through Alpaca's commission-free API.

### Why AlpacaDesk?

- **Local Security**: API keys never leave your machine (Windows Credential Manager)
- **No-Code Trading**: Visual strategy builder vs. coding required
- **Desktop Native**: Offline-capable vs. web-only platforms
- **Professional Tools**: Real-time streaming, backtesting, execution monitoring
- **Affordable**: Open source alternative to $127-254/mo competitors

## Key Features

- **Visual Strategy Builder**: Drag-and-drop blocks to create custom trading strategies
- **4 Pre-Built Strategies**: Momentum Breakout, Mean Reversion RSI, Dual MA, Bollinger Bands
- **Professional Backtesting**: Realistic simulation with slippage modeling and 13 performance metrics
- **Real-Time Data Streaming**: WebSocket-based live market data
- **Execution Quality Monitoring**: Track slippage, fill rates, and optimization insights
- **Strategy Scheduler**: Automated execution with configurable intervals
- **API Rate Limiting**: Token bucket algorithm prevents throttling
- **Comprehensive Settings**: 25+ configuration options across 6 categories
- **Local-First Security**: API keys stored using Windows DPAPI encryption
- **SQLite Persistence**: Complete data storage for strategies, orders, and history

## Tech Stack

- **Frontend**: Electron + React + TypeScript
- **Backend**: Python + FastAPI
- **Trading API**: Alpaca Markets
- **Database**: SQLite
- **Charting**: Lightweight Charts

## Development Setup

### Prerequisites

- Node.js 18+
- Python 3.10+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Homeless-Pets-Foundation/alpaca-trading.git
cd alpaca-trading
```

2. Install JavaScript dependencies:
```bash
npm install
```

3. Install Python dependencies:
```bash
cd engine
pip install -e ".[dev]"
cd ..
```

### Running in Development

Start both the Electron app and Python backend:

```bash
npm run dev
```

Or run them separately:

```bash
# Terminal 1 - Frontend
npm run dev:electron

# Terminal 2 - Backend
npm run dev:python
```

### Building for Production

```bash
npm run build
```

This will create a distributable Windows installer in the `release/` directory.

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Complete Feature Guide](README_COMPLETE.md)** - Comprehensive documentation (550+ lines)
- **[Development Guide](DEVELOPMENT.md)** - For developers and contributors
- **[Deployment Guide](DEPLOYMENT.md)** - Building and distributing
- **[Iteration Summaries](ITERATION_3_SUMMARY.md)** - Development progress tracking

## Quick Start

### 1. Get Alpaca API Keys
1. Sign up at [alpaca.markets](https://alpaca.markets)
2. Generate Paper Trading API keys
3. Save your Key ID and Secret Key

### 2. Install AlpacaDesk

**Development Mode:**
```bash
# Clone repository
git clone <repository-url>
cd alpaca-trading

# Install dependencies
npm install
cd engine && pip install -e ".[dev]" && cd ..

# Run application
npm run dev
```

**Production Mode:**
```bash
# Build installer
npm run build

# Install from release/AlpacaDesk Setup 1.0.0.exe
```

### 3. First Launch
1. Enter your Alpaca API Key ID and Secret
2. Select "Paper Trading" mode
3. Click "Connect"
4. Explore the dashboard

### 4. Deploy Your First Strategy
1. Navigate to **Strategies** tab
2. Select "Momentum Breakout" strategy
3. Click "Run Backtest" to see historical performance
4. If satisfied, click "Deploy to Paper"
5. Monitor execution in the **Overview** tab

## Project Structure

```
alpacadesk/
├── electron/              # Electron main process
├── src/                   # React frontend
│   ├── components/        # UI components
│   │   ├── builder/       # Visual strategy builder
│   │   ├── backtest/      # Backtesting UI
│   │   ├── execution/     # Execution quality dashboard
│   │   └── settings/      # Settings management
│   ├── services/          # API services
│   └── store/             # State management (Zustand)
├── engine/                # Python trading engine
│   └── src/alpacadesk_engine/
│       ├── api/           # FastAPI routes
│       ├── brokers/       # Broker integrations (Alpaca)
│       ├── strategies/    # Trading strategies
│       ├── backtest/      # Backtesting engine
│       ├── services/      # Background services (scheduler)
│       └── utils/         # Utilities (rate limiter, database)
└── resources/             # Static assets

Documentation:
├── README.md              # This file
├── README_COMPLETE.md     # Comprehensive feature guide
├── QUICKSTART.md          # Quick start guide
├── DEVELOPMENT.md         # Development guide
├── DEPLOYMENT.md          # Deployment guide
└── ITERATION_*_SUMMARY.md # Progress tracking
```

## Available Strategies

### 1. Momentum Breakout
Buys when price exceeds N-day high with volume confirmation. Ideal for trending markets.

### 2. Mean Reversion RSI
Enters when RSI is oversold and price is above 200MA. Capitalizes on temporary dips.

### 3. Dual Moving Average
Classic golden cross/death cross strategy with trend filter. Long-term systematic approach.

### 4. Bollinger Band Bounce
Buys at lower band bounces, sells at upper band touches. Mean reversion with volatility adaptation.

## License

ISC

## Disclaimer

**Trading involves substantial risk of loss.** This software is provided "as is" without warranty.

- Past performance does not guarantee future results
- Algorithmic trading can amplify losses
- Always understand what your strategies do before deploying
- Never invest more than you can afford to lose
- **Start with paper trading** (recommended 7+ days minimum)

## Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: See README_COMPLETE.md for detailed guides
- **Development**: See DEVELOPMENT.md for contribution guidelines

---

Built with Claude Code | Version 1.0.0 | Production Ready
