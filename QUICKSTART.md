# AlpacaDesk Quick Start Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18 or higher ([Download](https://nodejs.org/))
- **Python** 3.10 or higher ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Alpaca Account** (Sign up at [alpaca.markets](https://alpaca.markets))

## Step 1: Get Alpaca API Keys

1. Create a free account at [alpaca.markets](https://alpaca.markets)
2. Navigate to the API Keys page
3. Generate a **Paper Trading** API key (recommended for testing)
4. Save your API Key ID and Secret Key

> ⚠️ **Important**: Start with paper trading to test the platform without risking real money.

## Step 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/Homeless-Pets-Foundation/alpaca-trading.git
cd alpaca-trading

# Install JavaScript dependencies
npm install

# Install Python dependencies
cd engine
pip install -e ".[dev]"
cd ..
```

## Step 3: Run the Application

### Option A: Run Everything Together (Recommended)

```bash
npm run dev
```

This starts both the Electron app and Python backend automatically.

### Option B: Run Separately (For Debugging)

**Terminal 1 - Backend:**
```bash
cd engine
uvicorn src.alpacadesk_engine.main:app --reload --port 8765
```

**Terminal 2 - Frontend:**
```bash
npm run dev:electron
```

## Step 4: First Login

1. The AlpacaDesk window will open
2. Enter your Alpaca API credentials:
   - API Key ID: `PK...` (from Step 1)
   - Secret Key: Your secret key
   - Select **Paper Trading** (recommended)
3. Click "Connect & Continue"

## Step 5: Explore the Dashboard

After successful login, you'll see the main dashboard with:

- **Overview**: Portfolio value, buying power, active strategies
- **Strategies**: Pre-built algorithmic strategies
- **Builder**: Visual strategy builder (drag-and-drop)
- **Backtest**: Test strategies against historical data
- **Settings**: Configure preferences

## What's Working Now

✅ **Authentication** - Securely connect to Alpaca
✅ **Account Info** - View portfolio and positions
✅ **Order Execution** - Place market and limit orders
✅ **Pre-built Strategies** - Momentum and Mean Reversion
✅ **Strategy Management** - Create, enable, disable strategies
✅ **Local Security** - API keys stored in Windows Credential Manager

## What's In Progress

🚧 **Visual Strategy Builder** - Drag-and-drop interface
🚧 **Real-time Data** - WebSocket streaming
🚧 **Backtesting Engine** - Full historical simulation
🚧 **Performance Charts** - Equity curves and metrics

## Example: Deploy a Strategy

1. Go to the **Strategies** tab
2. Click on "Momentum Breakout"
3. Configure parameters:
   - Symbols: `SPY, QQQ, IWM`
   - Lookback Period: `20` days
   - Position Size: `10%` of portfolio
4. Click "Run Backtest" to see historical performance
5. If satisfied, click "Deploy to Paper"
6. Monitor in the Overview tab

## API Endpoints

The Python backend runs on `http://localhost:8765`. You can test endpoints:

```bash
# Health check
curl http://localhost:8765/health

# Get account info (after login)
curl http://localhost:8765/api/account/info

# List strategies
curl http://localhost:8765/api/strategies/list
```

Full API documentation: http://localhost:8765/docs

## Troubleshooting

### "Connection Error" on Login

- Verify your API keys are correct
- Check that you selected the right mode (Paper vs Live)
- Ensure you're connected to the internet
- Try regenerating your API keys on Alpaca

### Backend Won't Start

```bash
# Check if port 8765 is in use
netstat -ano | findstr :8765

# Kill any process using port 8765
# Then restart the backend
```

### "Not Authenticated" Errors

- Log out and log back in
- Check Windows Credential Manager for stored keys
- Clear credentials: `Run` → `control keymgr.dll`

### Blank Screen on Startup

- Open DevTools: `Ctrl+Shift+I`
- Check Console for errors
- Verify backend is running on port 8765

## Security Best Practices

1. **Always start with paper trading**
2. **Never share your API keys**
3. **Review all strategy configurations before deploying**
4. **Set position size limits** to manage risk
5. **Monitor your strategies regularly**

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/Homeless-Pets-Foundation/alpaca-trading/issues)
- **Documentation**: See `DEVELOPMENT.md` for technical details
- **Alpaca API**: [alpaca.markets/docs](https://alpaca.markets/docs)

## Next Steps

1. **Paper trade for 7 days** minimum before going live
2. **Backtest strategies** with at least 2 years of data
3. **Start small** - Use 5-10% position sizes initially
4. **Learn the PRD** - Read `ALPACADESK_PRD_v1.1.md` for full vision

## Disclaimer

**Trading involves substantial risk of loss.** This software is provided "as-is" without warranty.

- Past performance does not guarantee future results
- Algorithmic trading can amplify losses
- Always understand what your strategies do before deploying
- Never invest more than you can afford to lose

---

**Happy Trading! 🦙📈**
