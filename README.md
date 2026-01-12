# AlpacaDesk

Native Windows Algorithmic Trading Application

## Overview

AlpacaDesk is a desktop application that democratizes algorithmic trading for retail investors. It combines a visual no-code strategy builder with pre-built proven strategies, local security architecture, and real-time execution through Alpaca's commission-free API.

## Features

- **Local-First Security**: API keys stored securely using Windows Credential Manager
- **Pre-Built Strategies**: Ready-to-use algorithmic trading strategies
- **Visual Strategy Builder**: Create custom strategies with drag-and-drop blocks
- **Backtesting Engine**: Test strategies against historical data
- **Real-Time Execution**: WebSocket-based live trading

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

## Project Structure

```
alpacadesk/
├── electron/           # Electron main process
├── src/                # React frontend
│   ├── components/     # UI components
│   ├── services/       # API services
│   └── store/          # State management
├── engine/             # Python trading engine
│   └── src/
│       └── alpacadesk_engine/
│           ├── api/    # FastAPI routes
│           ├── brokers/# Broker integrations
│           └── strategies/ # Trading strategies
└── resources/          # Static assets
```

## License

ISC

## Disclaimer

Trading involves risk. This software is provided "as is" without warranty. Always test with paper trading before using real money.
