# Product Requirements Document (PRD)

## AlpacaDesk — Native Windows Algorithmic Trading Application

### Version 1.1 | January 2026

---

## 1. Executive Summary

### 1.1 Product Vision

**AlpacaDesk** is a native Windows desktop application that democratizes algorithmic trading for retail investors. It combines a visual no-code strategy builder with pre-built proven strategies, local security architecture, and real-time execution through Alpaca's commission-free API—eliminating the coding barrier that prevents 55% of interested traders from adopting automation.

### 1.2 Problem Statement

The retail algorithmic trading market ($3.5B, growing 12-14% CAGR) suffers from a fundamental accessibility gap:

| Current Reality | User Impact |
|-----------------|-------------|
| Most platforms require coding (Python, C#, MQL) | 55%+ of interested traders can't participate |
| Cloud platforms store API keys on remote servers | Security-conscious traders avoid automation entirely |
| No-code options are expensive ($127-254/mo) or limited (batch execution only) | Price-sensitive traders underserved |
| Alpaca has no native desktop application | 25,000+ developers lack polished consumer tooling |

**Target Users:** Security-conscious retail traders with $10,000-$250,000 portfolios who want systematic trading without learning to code.

### 1.3 Success Metrics

| Metric | Target (Year 1) | Target (Year 2) |
|--------|-----------------|-----------------|
| Monthly Active Users | 5,000 | 25,000 |
| Paid Conversion Rate | 8% | 12% |
| Monthly Recurring Revenue | $75,000 | $450,000 |
| User Retention (90-day) | 40% | 55% |
| App Store Rating | 4.3+ stars | 4.5+ stars |
| Average Strategy Win Rate | >52% (vs. buy-hold benchmark) | >54% |
| Customer Support Tickets/User | <0.5/month | <0.3/month |

### 1.4 Competitive Positioning

```
                        HIGH PRICE
                            │
          Trade Ideas       │       NinjaTrader
          ($178/mo)         │       (Code Required)
          No-Code ✓         │       
                            │
    ─────────────────────── ┼ ───────────────────────
    NO-CODE                 │                    CODE REQUIRED
                            │
         ┌──────────────┐   │       QuantConnect
         │  AlpacaDesk  │   │       (Free, Cloud)
         │   $39/mo     │   │
         │  Desktop ✓   │   │       Alpaca Raw API
         └──────────────┘   │       (Free, Code Required)
                            │
          Composer          │       
          ($32/mo, Web)     │       
          Batch Only        │
                            │
                        LOW PRICE
```

**Our Position:** Affordable no-code desktop application with real-time execution and local security—the only product in its quadrant.

---

## 2. Target User Personas

### 2.1 Primary Persona: "The Aspiring Systematic Trader"

| Attribute | Description |
|-----------|-------------|
| **Demographics** | Age 28-45, male-skewed (70/30), tech-adjacent profession |
| **Portfolio Size** | $25,000 - $150,000 |
| **Technical Level** | Comfortable with spreadsheets, not programming |
| **Trading Experience** | 2-5 years manual trading, frustrated with emotional decisions |
| **Current Tools** | Robinhood/Schwab for execution, TradingView for charts, spreadsheets for tracking |
| **Goals** | Remove emotion from trading, capture systematic edge, save time |
| **Pain Points** | "I know what strategy I want but can't code it"; "I don't trust cloud platforms with my API keys" |
| **Willingness to Pay** | $40-80/month if it saves 5+ hours/week and improves returns |

**Quote:** *"I've read about momentum strategies and they make sense, but every time I try to implement manually, I either miss entries or let emotions override the rules."*

### 2.2 Secondary Persona: "The Vibe Coder"

| Attribute | Description |
|-----------|-------------|
| **Demographics** | Age 22-35, software-adjacent but not professional developer |
| **Portfolio Size** | $10,000 - $75,000 |
| **Technical Level** | Can write basic Python, uses AI coding assistants |
| **Trading Experience** | 1-3 years, likely started during 2020-2021 retail boom |
| **Current Tools** | Alpaca API directly, Jupyter notebooks, Claude/ChatGPT for code |
| **Goals** | Graduate from fragile scripts to reliable automation |
| **Pain Points** | "My bot works until it doesn't"; "I spend more time debugging than trading" |
| **Willingness to Pay** | $25-50/month for reliability and saved debugging time |

**Quote:** *"I have a working Python script but it breaks every few weeks. I want something I can set and forget."*

### 2.3 Tertiary Persona: "The Time-Constrained Professional"

| Attribute | Description |
|-----------|-------------|
| **Demographics** | Age 35-55, high-income professional (doctor, lawyer, executive) |
| **Portfolio Size** | $100,000 - $500,000 |
| **Technical Level** | Low; values simplicity over customization |
| **Trading Experience** | Passive investor wanting more active management without time commitment |
| **Current Tools** | Wealth management apps, maybe a robo-advisor |
| **Goals** | Beat passive indexing without becoming a full-time trader |
| **Pain Points** | "I have 30 minutes a week for investing, max" |
| **Willingness to Pay** | $75-150/month if performance justifies it |

**Quote:** *"I don't want to learn trading—I want results. Show me strategies that work and let me turn them on."*

---

## 3. Challenge Mitigation Strategies

### 3.1 Challenge: Alpaca Execution Complaints (Slow Fills, Slippage)

**Root Causes:**
- Payment for order flow (PFOF) routing to market makers
- Market orders during volatility
- Stop orders triggering at unfavorable prices

**Mitigation Strategies:**

| Strategy | Implementation | User Benefit |
|----------|----------------|--------------|
| **Intelligent Order Types** | Default to limit orders with smart pricing (midpoint + buffer) | Reduces slippage by 60-80% vs. market orders |
| **Slippage Monitoring** | Track expected vs. actual fill prices; alert users to patterns | Transparency builds trust; users can adjust strategies |
| **Execution Time Optimization** | Avoid first/last 15 minutes of trading day for non-urgent orders | Reduces volatility-driven slippage |
| **Order Simulation Mode** | Show "what would have happened" before live deployment | Users see realistic execution expectations |
| **Adaptive Limit Pricing** | Automatically adjust limit prices based on volatility (ATR-based) | Better fills in choppy markets |
| **Multi-Broker Support (Phase 2)** | Add Interactive Brokers and Tradier as alternatives | Users can switch if Alpaca quality degrades |

**UI Implementation:**
```
┌─────────────────────────────────────────────────────────────┐
│  📊 EXECUTION QUALITY DASHBOARD                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Last 30 Days Performance:                                   │
│  ├── Orders Executed: 47                                     │
│  ├── Avg Slippage: -0.03% (vs. -0.15% market order avg)     │
│  ├── Fill Rate: 94.2%                                        │
│  └── Unfilled (expired): 3 orders                            │
│                                                              │
│  ⚠️ Recommendation: Your TSLA orders show 0.12% avg          │
│     slippage. Consider using limit orders with 0.1%          │
│     buffer for this volatile ticker.                         │
│                                                              │
│  [View Detailed Report]  [Adjust Order Settings]             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Challenge: API Rate Limits (200 requests/minute)

**Root Causes:**
- Alpaca enforces 200 req/min for standard accounts
- Naive implementations poll repeatedly for updates
- Multi-symbol strategies multiply API calls

**Mitigation Strategies:**

| Strategy | Implementation | API Savings |
|----------|----------------|-------------|
| **WebSocket-First Architecture** | Use streaming for all real-time data (quotes, trades, order updates) | 90%+ reduction in REST calls |
| **Intelligent Caching** | Cache account/positions data with TTL; refresh only when needed | Eliminates redundant calls |
| **Batch Operations** | Combine multiple order submissions where possible | 5-10x fewer calls for multi-leg strategies |
| **Request Budgeting** | Track API usage in real-time; queue low-priority requests | Prevents rate limit errors |
| **Strategy Frequency Limits** | Enforce minimum intervals between strategy evaluations | Aligns with moderate-frequency positioning |

**Architecture Diagram:**
```
┌─────────────────────────────────────────────────────────────┐
│                     AlpacaDesk Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐     WebSocket (Streaming)                  │
│   │   Alpaca    │ ◄──────────────────────────────────────┐   │
│   │   Servers   │                                        │   │
│   └─────────────┘ ───────────────────────────────────►   │   │
│         │              REST API (Orders/Account)         │   │
│         │                                                │   │
│         ▼                                                │   │
│   ┌─────────────────────────────────────────────────┐   │   │
│   │              CONNECTION MANAGER                  │   │   │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │   │   │
│   │  │WebSocket│  │  REST   │  │ Rate Limiter    │ │   │   │
│   │  │ Client  │  │ Client  │  │ (Token Bucket)  │ │   │   │
│   │  └─────────┘  └─────────┘  └─────────────────┘ │   │   │
│   └─────────────────────────────────────────────────┘   │   │
│         │                                                │   │
│         ▼                                                │   │
│   ┌─────────────────────────────────────────────────┐   │   │
│   │                 LOCAL CACHE                      │   │   │
│   │  • Positions (TTL: 5s)                          │   │   │
│   │  • Account (TTL: 30s)                           │   │   │
│   │  • Historical Data (TTL: 1 day)                 │   │   │
│   │  • Order Status (WebSocket-updated)             │   │   │
│   └─────────────────────────────────────────────────┘   │   │
│         │                                                │   │
│         ▼                                                │   │
│   ┌─────────────────────────────────────────────────┐   │   │
│   │              STRATEGY ENGINE                     │◄──┘   │
│   │  • Evaluates conditions against cached data     │       │
│   │  • Triggers orders via REST (rate-limited)      │       │
│   │  • Max evaluation frequency: 1/minute default   │       │
│   └─────────────────────────────────────────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**User-Facing Rate Limit Display:**
```
┌────────────────────────────────────────┐
│  API Usage: ████████░░ 156/200         │
│  Resets in: 34 seconds                 │
│  Status: ✅ Healthy                     │
└────────────────────────────────────────┘
```

### 3.3 Challenge: Competition from TradingView

**TradingView Strengths:**
- Best-in-class charting (free tier)
- Massive community and indicator library
- Cross-broker integration
- Brand recognition

**Our Counter-Positioning:**

| TradingView Weakness | AlpacaDesk Advantage |
|----------------------|----------------------|
| Alerts require webhooks + third-party execution | Native integrated execution—no middleware |
| Pine Script learning curve for custom strategies | Visual builder—truly zero code |
| Cloud-based (API keys on their servers) | Local-only architecture—keys never leave your machine |
| Subscription required for multiple alerts | Unlimited strategies in paid tier |
| No backtesting on price action (only indicators) | Full historical backtesting with realistic execution modeling |
| Web-based (no offline capability) | Native desktop—works offline for analysis |

**Positioning Statement:** *"TradingView is for charting. AlpacaDesk is for automated execution. Use both—we integrate with TradingView alerts as an input source."*

**Integration Strategy:**
- Accept TradingView webhook alerts as strategy triggers
- Embed TradingView's free charting widget for basic charts
- Differentiate on execution, backtesting, and security

### 3.4 Challenge: User Education for Non-Technical Users

**The Onboarding Problem:**
- Algo trading concepts are inherently complex
- Users need to understand risk before deploying real money
- Poor onboarding → high churn and support costs

**Mitigation Strategies:**

| Strategy | Implementation |
|----------|----------------|
| **Strongly Encouraged Paper Trading** | New users see prominent recommendation for 7-day paper trading; can skip with explicit risk acknowledgment |
| **Interactive Strategy Tutorials** | Guided walkthroughs for each pre-built strategy type |
| **Contextual Help Everywhere** | Hover tooltips, "Learn More" links, embedded videos |
| **Progressive Disclosure** | Simple mode by default; advanced features unlocked over time |
| **Risk Warnings with Friction** | Clear warnings before live deployment; require acknowledgment |
| **Community + Templates** | Learn from others' (anonymized) successful configurations |

**Onboarding Flow (Updated - Paper Trading Strongly Encouraged, Not Mandatory):**
```
┌─────────────────────────────────────────────────────────────┐
│                    ALPACADESK ONBOARDING                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Step 1: Connect Alpaca Account                              │
│  ════════════════════════════════════════════════════════    │
│  [■■■■■■■■■■░░░░░░░░░░░░░░░░░░░░] 33%                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                                                        │  │
│  │  🔐 YOUR API KEYS STAY ON THIS COMPUTER                │  │
│  │                                                        │  │
│  │  Unlike cloud platforms, AlpacaDesk stores your        │  │
│  │  credentials locally using Windows encryption.         │  │
│  │  We never see or transmit your keys.                   │  │
│  │                                                        │  │
│  │  API Key ID:     [________________________]            │  │
│  │  Secret Key:     [________________________]            │  │
│  │                                                        │  │
│  │  ☑ I'm using a PAPER trading account (recommended)     │  │
│  │  ☐ I'm using a LIVE trading account                    │  │
│  │                                                        │  │
│  │  [Get API Keys from Alpaca ↗]                          │  │
│  │                                                        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  📚 New to Alpaca? [Watch 2-min setup video]                 │
│                                                              │
│                              [Back]  [Connect & Continue →]  │
└─────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────┐
│  Step 2: Choose Your Path                                    │
│  ════════════════════════════════════════════════════════    │
│  [■■■■■■■■■■■■■■■■■■■░░░░░░░░░░░] 66%                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                                                         ││
│  │  ⭐ RECOMMENDED: Start with Paper Trading               ││
│  │                                                         ││
│  │  Practice with virtual money for 7 days to:            ││
│  │  • Learn the platform without risk                     ││
│  │  • Test your strategies in real market conditions      ││
│  │  • Build confidence before using real money            ││
│  │                                                         ││
│  │  📊 Users who paper trade first lose 67% less money    ││
│  │     in their first month of live trading.              ││
│  │                                                         ││
│  │              [Start Paper Trading →]                    ││
│  │                                                         ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ─────────────────────── OR ───────────────────────────────  │
│                                                              │
│  I'm experienced and want to start with live trading:        │
│                                                              │
│  ⚠️ Before proceeding, please acknowledge:                   │
│                                                              │
│  □ I understand algorithmic trading carries substantial     │
│    risk of financial loss                                   │
│  □ I have experience with trading and understand market     │
│    mechanics                                                │
│  □ I accept full responsibility for any losses incurred     │
│  □ I have read and understand the risk disclosure           │
│                                                              │
│  [Skip to Live Trading →] (Requires all checkboxes)         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Core Features

### 4.1 Authentication & Security (P0 — Launch Blocker)

**Local-First Security Architecture:**

| Feature | Implementation | Security Benefit |
|---------|----------------|------------------|
| **Windows Credential Manager** | API keys stored via Windows DPAPI | Encryption tied to Windows login; keys inaccessible to other apps |
| **Never-Transmit Policy** | Keys used only for direct Alpaca API calls | Zero attack surface on our servers (we have none) |
| **Session Encryption** | OAuth tokens encrypted at rest | Protects against local disk access |
| **Optional 2FA Gate** | Require Windows Hello/PIN before launching | Prevents unauthorized access on shared computers |
| **Audit Logging** | All API calls logged locally with timestamps | User can verify no unauthorized activity |

**Security Comparison Marketing:**
```
┌─────────────────────────────────────────────────────────────┐
│           WHERE ARE YOUR API KEYS STORED?                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Cloud Platforms (Composer, TradersPost, etc.):              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Your Computer → Internet → Their Servers → Alpaca    │  │
│  │                              ⚠️ Keys stored here       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  AlpacaDesk:                                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Your Computer ─────────────────────────────→ Alpaca  │  │
│  │  🔐 Keys stay here                                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Pre-Built Strategy Library (P0 — Core Value Proposition)

**Launch Strategies (5 proven approaches):**

| Strategy | Description | Parameters | Typical Trades/Month |
|----------|-------------|------------|----------------------|
| **Momentum Breakout** | Buy when price exceeds N-day high with volume confirmation | Lookback period, volume multiplier, position size | 5-15 |
| **Mean Reversion RSI** | Buy when RSI oversold + price above 200MA; sell when RSI overbought | RSI period, oversold/overbought thresholds | 10-25 |
| **Dual Moving Average** | Classic golden/death cross with trend filter | Fast MA, slow MA, trend MA | 3-8 |
| **Bollinger Band Bounce** | Buy at lower band with confirmation; sell at upper band | BB period, std dev, confirmation candles | 8-20 |
| **Relative Strength Rotation** | Monthly rotation into top N performers from watchlist | Lookback period, number of holdings, rebalance frequency | 2-5 |

**Strategy Card UI:**
```
┌─────────────────────────────────────────────────────────────┐
│  📈 MOMENTUM BREAKOUT                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Buy when price breaks above the highest high of the past    │
│  N days, confirmed by above-average volume.                  │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  [Chart showing example breakout pattern]               ││
│  │                                                         ││
│  │         ╱╲    ←── Entry point                           ││
│  │   ╱╲   ╱  ╲   ←── Breakout above resistance             ││
│  │  ╱  ╲_╱    ╲                                            ││
│  │ ╱           ╲___                                        ││
│  │╱                                                        ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  BACKTEST RESULTS (SPY, 5 years):                           │
│  ├── Total Return: +127% (vs. +89% buy-and-hold)            │
│  ├── Max Drawdown: -18% (vs. -34% buy-and-hold)             │
│  ├── Win Rate: 58%                                          │
│  ├── Avg Trade Duration: 12 days                            │
│  └── Sharpe Ratio: 1.2                                      │
│                                                              │
│  ⚠️ Past performance does not guarantee future results.      │
│                                                              │
│  CONFIGURABLE PARAMETERS:                                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Lookback Period:    [20] days    (Range: 10-50)       │ │
│  │  Volume Multiplier:  [1.5]x avg   (Range: 1.0-3.0)     │ │
│  │  Position Size:      [10]% of portfolio                │ │
│  │  Stop Loss:          [5]% below entry                  │ │
│  │  Take Profit:        [15]% above entry (optional)      │ │
│  │  Max Positions:      [5] concurrent                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  [📊 Run Backtest]  [📝 Customize]  [▶️ Deploy to Paper]     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Visual Strategy Builder — Complete UI/UX Specification

### 5.1 Design Philosophy

The Visual Strategy Builder is AlpacaDesk's primary differentiator. It must:

1. **Feel intuitive within 5 minutes** — No tutorials required for basic use
2. **Scale from simple to sophisticated** — Beginners and power users both served
3. **Prevent dangerous mistakes** — Guard rails that don't feel restrictive
4. **Generate readable logic** — Users understand what their strategy does
5. **Match mental models** — "If this happens, then do that" natural language flow

### 5.2 Builder Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🔧 STRATEGY BUILDER                                    [Save] [Test] [Deploy]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐ ┌────────────────────────────────────────────────────┐│
│  │   BLOCK PALETTE  │ │                    CANVAS                          ││
│  │   ────────────── │ │                                                    ││
│  │                  │ │    ┌─────────────────┐                             ││
│  │  ⏰ TRIGGERS     │ │    │    ⏰ TRIGGER   │                             ││
│  │  ├─ Time Interval│ │    │  Every 15 min   │                             ││
│  │  ├─ Market Open  │ │    │  [Edit]         │                             ││
│  │  ├─ Market Close │ │    └────────┬────────┘                             ││
│  │  ├─ Price Alert  │ │             │                                      ││
│  │  └─ Webhook      │ │             ▼                                      ││
│  │                  │ │    ┌─────────────────┐                             ││
│  │  🔍 UNIVERSE     │ │    │  🔍 UNIVERSE    │                             ││
│  │  ├─ Watchlist    │ │    │  Tech Leaders   │                             ││
│  │  ├─ S&P 500      │ │    │  (AAPL, MSFT,   │                             ││
│  │  ├─ NASDAQ 100   │ │    │   GOOGL, NVDA)  │                             ││
│  │  ├─ Sector ETFs  │ │    │  [Edit]         │                             ││
│  │  └─ Custom List  │ │    └────────┬────────┘                             ││
│  │                  │ │             │                                      ││
│  │  📊 CONDITIONS   │ │             ▼                                      ││
│  │  ├─ Price vs MA  │ │    ┌─────────────────┐                             ││
│  │  ├─ RSI Level    │ │    │ 📊 CONDITION    │                             ││
│  │  ├─ MACD Cross   │ │    │                 │                             ││
│  │  ├─ Volume Spike │ │    │ IF Price > 20MA │                             ││
│  │  ├─ Bollinger    │ │    │ AND RSI < 70    │                             ││
│  │  ├─ ATR Filter   │ │    │ AND Volume >1.5x│                             ││
│  │  └─ Custom...    │ │    │ [Edit]          │                             ││
│  │                  │ │    └────────┬────────┘                             ││
│  │  📈 ACTIONS      │ │             │                                      ││
│  │  ├─ Buy          │ │      ┌──────┴──────┐                               ││
│  │  ├─ Sell         │ │      │             │                               ││
│  │  ├─ Set Stop     │ │      ▼             ▼                               ││
│  │  ├─ Set Target   │ │  ┌───────┐    ┌───────┐                            ││
│  │  ├─ Close All    │ │  │✅ TRUE │    │❌ FALSE│                            ││
│  │  └─ Notify       │ │  └───┬───┘    └───┬───┘                            ││
│  │                  │ │      │            │                                ││
│  │  🔀 FLOW         │ │      ▼            ▼                                ││
│  │  ├─ If/Then/Else │ │  ┌────────┐  ┌────────┐                            ││
│  │  ├─ Wait         │ │  │📈 BUY   │  │⏭️ SKIP  │                            ││
│  │  ├─ Loop         │ │  │Limit    │  │        │                            ││
│  │  └─ Exit         │ │  │5% size  │  │        │                            ││
│  │                  │ │  │[Edit]   │  │        │                            ││
│  │  [+ Custom Block]│ │  └────────┘  └────────┘                            ││
│  │                  │ │                                                    ││
│  └──────────────────┘ │  ─────────────────────────────────────────────────││
│                       │                                                    ││
│                       │  📝 STRATEGY SUMMARY (Auto-generated):             ││
│                       │  "Every 15 minutes, for each symbol in Tech        ││
│                       │   Leaders where price > 20-day MA, RSI < 70,       ││
│                       │   and volume > 1.5x average: BUY with limit        ││
│                       │   order at 5% of portfolio."                       ││
│                       │                                                    ││
│                       └────────────────────────────────────────────────────┘│
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│  VALIDATION: ✅ Strategy is valid    │  Est. trades/month: 8-15  │  Risk: Med │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Block Types — Detailed Specifications

#### 5.3.1 Trigger Blocks

Triggers define WHEN the strategy evaluates. Only one trigger per strategy.

```
┌─────────────────────────────────────────────────────────────┐
│  ⏰ TIME INTERVAL TRIGGER                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Check conditions every:                                     │
│                                                              │
│  ○ 1 minute        ○ 15 minutes      ○ 1 hour               │
│  ○ 5 minutes       ○ 30 minutes      ○ 4 hours              │
│                                                              │
│  ☑ Only during market hours (9:30 AM - 4:00 PM ET)          │
│  ☐ Include pre-market (4:00 AM - 9:30 AM ET)                │
│  ☐ Include after-hours (4:00 PM - 8:00 PM ET)               │
│                                                              │
│  ℹ️ Shorter intervals = more API usage. 15 min recommended.  │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🔔 PRICE ALERT TRIGGER                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Trigger when:                                               │
│                                                              │
│  Symbol: [AAPL    ▼]                                        │
│                                                              │
│  ○ Price crosses above  [$_____ ]                           │
│  ○ Price crosses below  [$_____ ]                           │
│  ○ Price changes by     [_____%] in [__] minutes            │
│  ○ Volume exceeds       [_____] shares                      │
│                                                              │
│  ℹ️ Uses WebSocket streaming - no API rate limit impact.     │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📡 WEBHOOK TRIGGER (TradingView Integration)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Your webhook URL:                                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ http://localhost:9876/hook/strat_abc123                 ││
│  └─────────────────────────────────────────────────────────┘│
│  [Copy URL]                                                  │
│                                                              │
│  Expected payload format:                                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ {                                                       ││
│  │   "action": "buy" | "sell",                             ││
│  │   "symbol": "AAPL",                                     ││
│  │   "price": 185.50  (optional)                           ││
│  │ }                                                       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ☑ Validate payload before executing                        │
│  ☑ Log all received webhooks                                │
│                                                              │
│  [Test Webhook]                        [Cancel] [Apply]      │
└─────────────────────────────────────────────────────────────┘
```

#### 5.3.2 Universe Blocks

Universe defines WHAT symbols the strategy evaluates.

```
┌─────────────────────────────────────────────────────────────┐
│  🔍 UNIVERSE SELECTOR                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Strategy will evaluate:                                     │
│                                                              │
│  ○ My Watchlist                                             │
│    └─ Select: [Tech Leaders ▼] (12 symbols)                 │
│                                                              │
│  ○ Index Components                                         │
│    └─ [S&P 500 ▼] [NASDAQ 100] [Dow 30] [Russell 2000]     │
│                                                              │
│  ○ Sector ETFs                                              │
│    └─ ☐ XLK (Tech)  ☐ XLF (Finance)  ☐ XLV (Health)        │
│       ☐ XLE (Energy) ☐ XLI (Industrial) ☐ XLY (Consumer)   │
│                                                              │
│  ○ Custom Symbols                                           │
│    └─ [AAPL, MSFT, GOOGL, NVDA, AMD____________]           │
│                                                              │
│  ○ Dynamic Screen (Pro)                                     │
│    └─ Top [10] by [52-week performance ▼]                   │
│       from [S&P 500 ▼]                                      │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│  Selected: 12 symbols                                        │
│  ⚠️ Large universes (>50) may hit rate limits.              │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘
```

#### 5.3.3 Condition Blocks

Conditions define IF rules using technical and fundamental filters.

```
┌─────────────────────────────────────────────────────────────┐
│  📊 CONDITION BUILDER                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Entry conditions (ALL must be true):                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 1. [Price      ▼] [is above    ▼] [SMA      ▼] [(20)  ]││
│  │    └─ Price is above 20-day Simple Moving Average       ││
│  │                                                    [🗑️] ││
│  └─────────────────────────────────────────────────────────┘│
│                             AND                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 2. [RSI (14)   ▼] [is below    ▼] [Value    ▼] [(70)  ]││
│  │    └─ 14-period RSI is below 70 (not overbought)        ││
│  │                                                    [🗑️] ││
│  └─────────────────────────────────────────────────────────┘│
│                             AND                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 3. [Volume     ▼] [is above    ▼] [Avg Vol  ▼] [×(1.5)]││
│  │    └─ Current volume is 1.5x 20-day average volume      ││
│  │                                                    [🗑️] ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  [+ Add Condition]                                           │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│  ☐ Use OR logic (any condition true)                        │
│  ☐ Add NOT IN POSITION filter (avoid duplicate entries)     │
│                                                              │
│  AVAILABLE INDICATORS:                                       │
│  Price: Close, Open, High, Low, VWAP                        │
│  Moving Averages: SMA, EMA, WMA (any period)                │
│  Momentum: RSI, MACD, Stochastic, ROC, MFI                  │
│  Volatility: Bollinger Bands, ATR, Keltner                  │
│  Volume: Volume, OBV, VWAP, Avg Volume                      │
│  Trend: ADX, Aroon, Parabolic SAR                           │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘
```

**Condition Operator Reference:**

| Left Side | Operators | Right Side |
|-----------|-----------|------------|
| Price, Indicator Value | is above, is below, crosses above, crosses below, equals | Fixed Value, Another Indicator, Moving Average |
| Volume | is above, is below | Fixed Value, Average Volume × multiplier |
| RSI, Stochastic | is above, is below, is between | Fixed Value (0-100) |
| MACD | crosses above, crosses below, is above, is below | Signal Line, Zero Line |
| Bollinger | price touches, price above, price below | Upper Band, Lower Band, Middle Band |

#### 5.3.4 Action Blocks

Actions define WHAT to do when conditions are met.

```
┌─────────────────────────────────────────────────────────────┐
│  📈 BUY ACTION                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Order Type:                                                 │
│  ○ Market Order (immediate, may have slippage)              │
│  ● Limit Order (recommended)                                │
│    └─ Price: ○ Current bid  ● Current price  ○ Custom       │
│       └─ Buffer: [+0.05]% above current (for fills)         │
│  ○ Stop Order (trigger at price)                            │
│                                                              │
│  Position Size:                                              │
│  ○ Fixed Dollar Amount: [$________]                         │
│  ● Percentage of Portfolio: [5]%                            │
│  ○ Fixed Shares: [___] shares                               │
│  ○ Risk-Based (Pro): Risk [1]% with stop at [___]          │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│  Attached Orders (Optional):                                 │
│                                                              │
│  ☑ Stop Loss                                                │
│    └─ [5]% below entry price                                │
│    └─ ○ Trailing stop: trail by [___]%                      │
│                                                              │
│  ☑ Take Profit                                              │
│    └─ [15]% above entry price                               │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│  Guardrails:                                                 │
│  ☑ Max positions in this strategy: [5]                      │
│  ☑ Don't buy if already holding this symbol                 │
│  ☐ Only buy if no open orders for this symbol               │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📉 SELL ACTION                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  What to sell:                                               │
│  ● Current symbol (from strategy scan)                      │
│  ○ Specific symbol: [________]                              │
│  ○ All positions in this strategy                           │
│  ○ Oldest position                                          │
│                                                              │
│  How much to sell:                                           │
│  ● Entire position (100%)                                   │
│  ○ Partial: [___]% of position                              │
│  ○ Fixed shares: [___] shares                               │
│                                                              │
│  Order Type:                                                 │
│  ○ Market Order                                             │
│  ● Limit Order                                              │
│    └─ Price: Current bid - [0.02]% buffer                   │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🔔 NOTIFY ACTION                                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Send notification when conditions are met:                  │
│                                                              │
│  ☑ Desktop notification (Windows)                           │
│  ☐ Email to: [________________________]                     │
│  ☐ Webhook to: [________________________]                   │
│                                                              │
│  Message template:                                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ {{strategy_name}}: {{action}} signal for {{symbol}}     ││
│  │ at ${{price}} on {{datetime}}                           ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ☐ Notify only (don't execute trade)                        │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘
```

#### 5.3.5 Flow Control Blocks

```
┌─────────────────────────────────────────────────────────────┐
│  🔀 IF / THEN / ELSE                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  This block creates two paths based on conditions:           │
│                                                              │
│            ┌─────────────┐                                   │
│            │ CONDITIONS  │                                   │
│            │  (defined   │                                   │
│            │   above)    │                                   │
│            └──────┬──────┘                                   │
│                   │                                          │
│           ┌───────┴───────┐                                  │
│           ▼               ▼                                  │
│      ┌────────┐      ┌────────┐                             │
│      │  TRUE  │      │ FALSE  │                             │
│      │ (drag  │      │ (drag  │                             │
│      │ actions│      │ actions│                             │
│      │  here) │      │  here) │                             │
│      └────────┘      └────────┘                             │
│                                                              │
│  TRUE path: Execute these actions when conditions pass       │
│  FALSE path: Execute these actions when conditions fail      │
│             (Leave empty to do nothing)                      │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ⏳ WAIT BLOCK                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Pause strategy execution for:                               │
│                                                              │
│  [___] ○ seconds  ○ minutes  ○ hours  ○ days                │
│                                                              │
│  Use case: Wait after entry before checking exit conditions  │
│                                                              │
│  ⚠️ Strategy won't evaluate other symbols during wait.       │
│                                                              │
│                                          [Cancel] [Apply]    │
└─────────────────────────────────────────────────────────────┘
```

### 5.4 Canvas Interactions

**Drag and Drop:**
- Drag blocks from palette to canvas
- Drop on connection points (highlighted when dragging)
- Blocks snap to grid for alignment

**Block Connections:**
- Click output port → click input port to connect
- Lines auto-route around other blocks
- Click line to delete connection

**Block Editing:**
- Double-click block to open edit modal
- Right-click for context menu (duplicate, delete, disable)
- Keyboard shortcuts: Del (delete), Ctrl+D (duplicate), Ctrl+Z (undo)

**Canvas Controls:**
- Scroll/drag to pan
- Ctrl+scroll to zoom
- Minimap in corner for navigation
- Auto-arrange button for cleanup

### 5.5 Validation System

The builder validates strategy logic in real-time:

```
┌─────────────────────────────────────────────────────────────┐
│  STRATEGY VALIDATION                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ PASSED CHECKS:                                           │
│  ├── Trigger block present                                   │
│  ├── At least one action block                               │
│  ├── All blocks connected                                    │
│  ├── No circular dependencies                                │
│  └── Position sizing within limits                           │
│                                                              │
│  ⚠️ WARNINGS:                                                │
│  ├── No stop loss configured (recommended for risk mgmt)    │
│  └── Large universe (87 symbols) may cause rate limiting    │
│                                                              │
│  ❌ ERRORS (must fix):                                       │
│  └── Condition block has no connected action                 │
│                                                              │
│  Status: ⚠️ Valid with warnings                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Validation Rules:**

| Rule | Type | Message |
|------|------|---------|
| Must have trigger | Error | "Add a trigger block to define when strategy runs" |
| Must have action | Error | "Add at least one action (buy/sell/notify)" |
| All blocks connected | Error | "Block 'Condition 2' is not connected to flow" |
| Position size valid | Error | "Position size cannot exceed 100% of portfolio" |
| Has stop loss | Warning | "Consider adding stop loss for risk management" |
| Universe size | Warning | "Large universes (>50 symbols) may hit API limits" |
| Evaluation frequency | Warning | "1-minute intervals will use API quota quickly" |

### 5.6 Strategy Templates

Pre-configured templates users can start from:

```
┌─────────────────────────────────────────────────────────────┐
│  📚 STRATEGY TEMPLATES                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Start with a proven template and customize:                 │
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │  📈 Golden Cross    │  │  📊 RSI Oversold    │           │
│  │                     │  │                     │           │
│  │  Buy: 50MA > 200MA  │  │  Buy: RSI < 30      │           │
│  │  Sell: 50MA < 200MA │  │  Sell: RSI > 70     │           │
│  │                     │  │                     │           │
│  │  Trades: 2-4/year   │  │  Trades: 10-20/mo   │           │
│  │  [Use Template]     │  │  [Use Template]     │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │  🎯 Breakout Buy    │  │  📉 Bollinger Mean  │           │
│  │                     │  │     Reversion       │           │
│  │  Buy: New 20-day    │  │                     │           │
│  │       high + volume │  │  Buy: Price < Lower │           │
│  │  Sell: 10% profit   │  │  Sell: Price > Upper│           │
│  │        or 5% stop   │  │                     │           │
│  │                     │  │  Trades: 8-15/mo    │           │
│  │  [Use Template]     │  │  [Use Template]     │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │  🔄 Sector Rotation │  │  ⚡ Momentum Screen │           │
│  │                     │  │                     │           │
│  │  Monthly rotation   │  │  Daily: Top 5 by    │           │
│  │  to top 3 sectors   │  │  3-month momentum   │           │
│  │  by momentum        │  │  from S&P 500       │           │
│  │                     │  │                     │           │
│  │  [Use Template]     │  │  [Use Template]     │           │
│  └─────────────────────┘  └─────────────────────┘           │
│                                                              │
│  [Start from Blank]                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.7 Mobile-Responsive Considerations

While this is a desktop app, the strategy builder should be usable on smaller screens (laptops):

| Viewport | Layout Adaptation |
|----------|-------------------|
| < 1280px | Collapsible palette, smaller canvas |
| < 1024px | Palette becomes overlay/drawer |
| < 768px | Not supported (show warning) |

### 5.8 Accessibility Requirements

| Feature | Implementation |
|---------|----------------|
| Keyboard Navigation | Tab through blocks, Enter to edit, Arrow keys on canvas |
| Screen Reader | ARIA labels on all interactive elements |
| Color Blindness | Don't rely on color alone; use icons + labels |
| Focus Indicators | Clear focus rings on all interactive elements |
| Font Scaling | Respects Windows display scaling |

---

## 6. Monetization Strategy

### 6.1 Pricing Tiers (Updated)

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | Paper trading only, 2 pre-built strategies, 1 custom strategy slot, basic backtesting (1 year history), community support |
| **Core** | $39/month | Live trading, all pre-built strategies, 5 custom strategy slots, full backtesting (5+ years), email support, TradingView webhook integration |
| **Pro** | $79/month | Everything in Core + unlimited strategies, Monte Carlo simulation, export to Python code, priority support, multi-account support, multi-broker support (IB, Tradier) |
| **Lifetime** | $1,199 one-time | Pro tier forever, includes all future features, founding member benefits |

### 6.2 Annual Discount

| Tier | Monthly | Annual (20% off) | Savings |
|------|---------|------------------|---------|
| Core | $39/mo | $374/year ($31.17/mo) | $94/year |
| Pro | $79/mo | $758/year ($63.17/mo) | $190/year |

### 6.3 Revenue Projections (Updated)

| Month | Free Users | Paid Users | MRR | Assumptions |
|-------|------------|------------|-----|-------------|
| 1 | 500 | 20 | $1,100 | Launch, early adopters |
| 3 | 2,000 | 100 | $5,500 | Initial marketing push |
| 6 | 5,000 | 300 | $16,500 | Word of mouth growing |
| 12 | 12,000 | 800 | $44,000 | Established presence |
| 24 | 30,000 | 2,500 | $137,500 | Market leader in niche |

---

## 7. Development Sprint Plan (Claude Code Optimized)

### 7.1 Development Philosophy for Claude Code

Working with Claude Code requires a different approach than traditional development:

1. **Atomic, testable chunks** — Each ticket should be completable in one Claude Code session
2. **Clear acceptance criteria** — Claude needs explicit "done" conditions
3. **Interface-first design** — Define data contracts before implementation
4. **Incremental integration** — Small pieces that connect, not big modules that don't
5. **Test as you go** — Each ticket includes verification steps

### 7.2 Sprint Overview

| Phase | Duration | Focus | Tickets |
|-------|----------|-------|---------|
| **Phase 1: Foundation** | Weeks 1-4 | Core infrastructure, authentication, basic UI shell | 20 tickets |
| **Phase 2: Trading Core** | Weeks 5-8 | Alpaca integration, order management, paper trading | 18 tickets |
| **Phase 3: Strategy Engine** | Weeks 9-12 | Pre-built strategies, backtesting, execution | 16 tickets |
| **Phase 4: Visual Builder** | Weeks 13-16 | No-code builder, validation, templates | 14 tickets |
| **Phase 5: Polish & Launch** | Weeks 17-20 | Multi-broker, onboarding, testing, launch prep | 12 tickets |

---

### 7.3 Phase 1: Foundation (Weeks 1-4)

#### Week 1: Project Setup & Electron Shell

**Ticket 1.1: Initialize Electron + React Project**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: None

Description:
Create the base Electron application with React frontend using Vite.

Acceptance Criteria:
- [ ] `npm create vite` with React + TypeScript template
- [ ] Electron main process configured (electron-builder)
- [ ] Hot reload working for development
- [ ] Basic window launches with "Hello AlpacaDesk" text
- [ ] Package.json scripts: dev, build, package

Files to Create:
- package.json
- electron/main.ts
- electron/preload.ts
- src/App.tsx
- src/main.tsx
- vite.config.ts
- electron-builder.yml

Claude Code Prompt:
"Create a new Electron + React + TypeScript project using Vite. 
Set up electron-builder for packaging. Include hot reload for 
development. The app should open a window displaying 'Hello AlpacaDesk'.
Use modern Electron security practices (contextIsolation, nodeIntegration: false)."
```

**Ticket 1.2: Configure Tailwind CSS + Design System**
```
Priority: P0
Estimate: 1-2 hours
Dependencies: 1.1

Description:
Set up Tailwind CSS with AlpacaDesk color palette and typography.

Acceptance Criteria:
- [ ] Tailwind CSS installed and configured
- [ ] Custom color palette defined (dark theme)
- [ ] Typography scale defined
- [ ] Sample component renders correctly with styles

Design Tokens:
```css
colors: {
  background: '#0D1117',
  surface: '#161B22',
  surfaceHover: '#21262D',
  border: '#30363D',
  text: '#E6EDF3',
  textMuted: '#7D8590',
  primary: '#238636',    /* Green - buy/positive */
  danger: '#DA3633',     /* Red - sell/negative */
  warning: '#D29922',    /* Yellow - warnings */
  info: '#58A6FF',       /* Blue - info/links */
}
```

Claude Code Prompt:
"Add Tailwind CSS to the Electron React project. Configure a custom 
dark theme color palette for a trading application. Create a sample 
component showing the color palette and typography scale."
```

**Ticket 1.3: Create Main Navigation Shell**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.2

Description:
Build the main application layout with sidebar navigation.

Acceptance Criteria:
- [ ] Sidebar with navigation items (Dashboard, Strategies, Builder, Backtest, Settings)
- [ ] Icons for each nav item (use Lucide icons)
- [ ] Active state highlighting
- [ ] Main content area with router outlet
- [ ] Top bar with account status placeholder

UI Reference:
```
┌─────────┬────────────────────────────────────────┐
│ 🏠 Dash │                                        │
│ 📊 Strat│           [Main Content Area]          │
│ 🔧 Build│                                        │
│ 📈 Back │                                        │
│ ⚙️ Set  │                                        │
└─────────┴────────────────────────────────────────┘
```

Claude Code Prompt:
"Create a main application layout for AlpacaDesk with a sidebar 
navigation and content area. Use React Router for navigation. 
Include Dashboard, Strategies, Builder, Backtest, and Settings pages 
as placeholders. Style with Tailwind using the dark theme."
```

**Ticket 1.4: Set Up Python Trading Engine Structure**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.1

Description:
Create Python backend structure for trading logic with proper project layout.

Acceptance Criteria:
- [ ] Python project structure with src/alpacadesk_engine/
- [ ] pyproject.toml with dependencies (alpaca-py, pandas, numpy)
- [ ] Entry point script that starts local HTTP server
- [ ] Health check endpoint returns {"status": "ok"}
- [ ] Basic logging configured

Project Structure:
```
engine/
├── pyproject.toml
├── src/
│   └── alpacadesk_engine/
│       ├── __init__.py
│       ├── main.py          # Entry point, HTTP server
│       ├── api/
│       │   └── routes.py    # FastAPI routes
│       ├── services/
│       │   └── __init__.py
│       └── utils/
│           └── logging.py
└── tests/
    └── __init__.py
```

Claude Code Prompt:
"Create a Python trading engine project structure for AlpacaDesk. 
Use FastAPI for the local HTTP server. Include proper project layout 
with pyproject.toml. Create a health check endpoint. Configure logging."
```

**Ticket 1.5: Electron ↔ Python Bridge**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 1.1, 1.4

Description:
Create communication layer between Electron and Python engine.

Acceptance Criteria:
- [ ] Electron main process spawns Python engine on startup
- [ ] Python engine runs on configurable local port (default 9876)
- [ ] IPC handlers in preload script for API calls
- [ ] React hook useEngineAPI() for making calls
- [ ] Engine health check displayed in UI
- [ ] Graceful shutdown when app closes

Claude Code Prompt:
"Create a bridge between Electron and a Python FastAPI backend. 
Electron should spawn the Python process on startup and kill it on 
shutdown. Create IPC handlers for communication. Include a React 
hook for making API calls from components. Add error handling for 
when Python engine is not responding."
```

#### Week 2: Authentication & Credential Management

**Ticket 1.6: Windows Credential Manager Integration**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.1

Description:
Implement secure credential storage using Windows Credential Manager.

Acceptance Criteria:
- [ ] Install and configure keytar library
- [ ] CredentialService class with store/retrieve/delete methods
- [ ] Separate storage for paper and live credentials
- [ ] Credentials encrypted at rest via Windows DPAPI
- [ ] Unit tests for credential operations

API:
```typescript
interface CredentialService {
  storeCredentials(apiKey: string, secretKey: string, isPaper: boolean): Promise<void>;
  getCredentials(isPaper: boolean): Promise<{apiKey: string, secretKey: string} | null>;
  deleteCredentials(isPaper: boolean): Promise<void>;
  hasCredentials(isPaper: boolean): Promise<boolean>;
}
```

Claude Code Prompt:
"Implement secure credential storage for AlpacaDesk using the keytar 
library (Windows Credential Manager). Create a CredentialService class 
that can store, retrieve, and delete API credentials. Support separate 
storage for paper and live trading accounts. Include TypeScript types."
```

**Ticket 1.7: Authentication UI - Connect Account Screen**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 1.2, 1.3, 1.6

Description:
Build the UI for connecting Alpaca accounts.

Acceptance Criteria:
- [ ] Form with API Key and Secret Key inputs
- [ ] Password-style masking for secret key
- [ ] Paper/Live account toggle
- [ ] "Get API Keys" link to Alpaca dashboard
- [ ] Connect button with loading state
- [ ] Error display for invalid credentials
- [ ] Success state with redirect to dashboard

UI Reference: See onboarding flow in Section 3.4

Claude Code Prompt:
"Create an authentication screen for AlpacaDesk where users enter 
their Alpaca API credentials. Include inputs for API key and secret, 
a toggle for paper/live accounts, and proper form validation. Show 
loading state during verification. Style with Tailwind dark theme."
```

**Ticket 1.8: Alpaca API Client - Authentication**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.4

Description:
Create Python Alpaca client with authentication.

Acceptance Criteria:
- [ ] AlpacaClient class wrapping alpaca-py
- [ ] authenticate() method validates credentials
- [ ] get_account() returns account info
- [ ] Proper error handling for invalid credentials
- [ ] Rate limit handling basics

Claude Code Prompt:
"Create an AlpacaClient class in Python that wraps the alpaca-py 
library. Implement authentication that validates API credentials. 
Include methods to get account information. Handle errors for invalid 
credentials and rate limiting. Support both paper and live environments."
```

**Ticket 1.9: Authentication Flow Integration**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.5, 1.6, 1.7, 1.8

Description:
Wire up the full authentication flow end-to-end.

Acceptance Criteria:
- [ ] UI calls Python engine to validate credentials
- [ ] Valid credentials stored in Windows Credential Manager
- [ ] App remembers authentication state between sessions
- [ ] Settings page shows connected account status
- [ ] Disconnect button clears credentials
- [ ] Auto-connect on app startup if credentials exist

Claude Code Prompt:
"Integrate the authentication flow for AlpacaDesk. When user enters 
credentials, validate with Alpaca API via Python backend, store in 
Windows Credential Manager on success, and redirect to dashboard. 
On app startup, check for stored credentials and auto-connect."
```

#### Week 3: Portfolio Dashboard

**Ticket 1.10: Alpaca API Client - Portfolio Data**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.8

Description:
Extend Alpaca client with portfolio data methods.

Acceptance Criteria:
- [ ] get_positions() returns all current positions
- [ ] get_portfolio_history() returns equity curve data
- [ ] get_account_activities() returns recent trades
- [ ] Data models for Position, PortfolioHistory, Activity
- [ ] Caching layer with configurable TTL

Data Models:
```python
@dataclass
class Position:
    symbol: str
    qty: float
    market_value: float
    cost_basis: float
    unrealized_pl: float
    unrealized_plpc: float
    current_price: float
    
@dataclass
class PortfolioSnapshot:
    equity: float
    cash: float
    buying_power: float
    positions: List[Position]
    timestamp: datetime
```

Claude Code Prompt:
"Extend the AlpacaClient with methods to fetch portfolio data: 
positions, portfolio history, and recent activities. Create dataclass 
models for the data. Implement a simple caching layer to avoid 
redundant API calls."
```

**Ticket 1.11: Dashboard - Account Summary Card**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.9, 1.10

Description:
Build the account summary section of dashboard.

Acceptance Criteria:
- [ ] Total portfolio value with daily change
- [ ] Cash balance and buying power
- [ ] Day's P&L with percentage
- [ ] Color coding (green positive, red negative)
- [ ] Loading skeleton state
- [ ] Auto-refresh every 30 seconds

UI Reference:
```
┌─────────────────────────────────────────────────────────────┐
│  Account Value: $52,847.32        Today: +$312.45 (+0.59%)  │
│  Cash: $12,420.00                 Buying Power: $24,840.00  │
└─────────────────────────────────────────────────────────────┘
```

Claude Code Prompt:
"Create an AccountSummary component for the dashboard showing total 
portfolio value, cash balance, buying power, and daily P&L. Fetch 
data from the Python backend. Include loading states and auto-refresh. 
Use green/red coloring for positive/negative values."
```

**Ticket 1.12: Dashboard - Positions Table**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 1.10

Description:
Build sortable positions table component.

Acceptance Criteria:
- [ ] Table with columns: Symbol, Qty, Price, Value, Cost, P&L, P&L%
- [ ] Sortable by any column (click header)
- [ ] Color-coded P&L cells
- [ ] Empty state for no positions
- [ ] Click row to view symbol details (future)

Claude Code Prompt:
"Create a PositionsTable component showing all portfolio positions. 
Include columns for symbol, quantity, current price, market value, 
cost basis, unrealized P&L (dollar and percent). Make columns sortable. 
Use Tailwind for styling with proper dark theme colors."
```

**Ticket 1.13: Dashboard - Equity Chart**
```
Priority: P1
Estimate: 3-4 hours
Dependencies: 1.10

Description:
Add portfolio equity curve chart.

Acceptance Criteria:
- [ ] Line chart showing equity over time
- [ ] Time period selector (1D, 1W, 1M, 3M, 1Y, All)
- [ ] Tooltip showing value on hover
- [ ] Responsive sizing
- [ ] Loading state

Library: Use lightweight-charts (TradingView open source)

Claude Code Prompt:
"Add an equity curve chart to the dashboard using lightweight-charts 
library. Fetch portfolio history from backend. Include time period 
selector buttons. Show value tooltip on hover. Style to match dark theme."
```

**Ticket 1.14: Dashboard - Integration**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.11, 1.12, 1.13

Description:
Assemble dashboard components into complete view.

Acceptance Criteria:
- [ ] Layout combines summary, positions, and chart
- [ ] Responsive grid layout
- [ ] Global refresh button
- [ ] Last updated timestamp
- [ ] Error boundary for component failures

Claude Code Prompt:
"Create the complete Dashboard page combining AccountSummary, 
PositionsTable, and EquityChart components. Use CSS grid for layout. 
Add a refresh button and last-updated timestamp. Include error 
boundaries so one component failure doesn't break the whole page."
```

#### Week 4: WebSocket & Real-Time Data

**Ticket 1.15: WebSocket Manager - Infrastructure**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 1.8

Description:
Create WebSocket connection manager for real-time data.

Acceptance Criteria:
- [ ] WebSocketManager class handles connection lifecycle
- [ ] Auto-reconnect with exponential backoff
- [ ] Subscribe/unsubscribe to symbols
- [ ] Event emitter pattern for data distribution
- [ ] Connection status tracking

Claude Code Prompt:
"Create a WebSocketManager class in Python for Alpaca's streaming 
data. Handle connection, disconnection, and auto-reconnect with 
exponential backoff. Support subscribing to trade and quote updates 
for multiple symbols. Use asyncio for non-blocking operation."
```

**Ticket 1.16: Real-Time Price Updates**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.15

Description:
Stream live prices to the UI.

Acceptance Criteria:
- [ ] Dashboard subscribes to held position symbols
- [ ] Prices update in real-time in positions table
- [ ] Flash animation on price change
- [ ] Handle market closed state gracefully

Claude Code Prompt:
"Implement real-time price updates for the positions table. Subscribe 
to WebSocket quotes for held symbols. Push updates to the Electron UI 
via the IPC bridge. Add a brief flash animation when prices change."
```

**Ticket 1.17: Order Updates Stream**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.15

Description:
Stream order status updates.

Acceptance Criteria:
- [ ] Subscribe to trade_updates stream
- [ ] Emit events for: new, fill, partial_fill, canceled, rejected
- [ ] Store order state in local cache
- [ ] UI notification on order events

Claude Code Prompt:
"Implement order status streaming using Alpaca's trade_updates 
WebSocket channel. Create an OrderUpdateHandler that processes 
events and maintains order state. Send notifications to the UI 
when orders are filled, canceled, or rejected."
```

**Ticket 1.18: Connection Status UI**
```
Priority: P1
Estimate: 1-2 hours
Dependencies: 1.15, 1.16

Description:
Show connection status in UI header.

Acceptance Criteria:
- [ ] Status indicator: Connected (green), Connecting (yellow), Disconnected (red)
- [ ] Tooltip showing details
- [ ] Click to force reconnect

UI:
```
┌────────────────────────────────────┐
│  🟢 Connected to Alpaca (Paper)    │
└────────────────────────────────────┘
```

Claude Code Prompt:
"Add a connection status indicator to the app header showing WebSocket 
connection state. Use colored dots (green=connected, yellow=connecting, 
red=disconnected). Include tooltip with details and click to reconnect."
```

**Ticket 1.19: Rate Limiter Implementation**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.8

Description:
Implement rate limiting for REST API calls.

Acceptance Criteria:
- [ ] Token bucket algorithm (200 tokens/minute)
- [ ] Queue requests when near limit
- [ ] Expose current usage via API
- [ ] Log warnings when approaching limit

Claude Code Prompt:
"Implement a rate limiter for Alpaca API calls using token bucket 
algorithm. Limit to 200 requests per minute. Queue requests when 
bucket is empty. Provide method to check current usage. Log warnings 
at 80% capacity."
```

**Ticket 1.20: API Usage Dashboard Widget**
```
Priority: P1
Estimate: 1-2 hours
Dependencies: 1.19

Description:
Display API usage in UI.

Acceptance Criteria:
- [ ] Progress bar showing usage (0-200)
- [ ] Resets countdown
- [ ] Warning state at 80%+

Claude Code Prompt:
"Create an APIUsageWidget component showing current API rate limit 
usage as a progress bar. Show requests remaining and time until reset. 
Change color to warning (yellow) at 80% usage."
```

---

### 7.4 Phase 2: Trading Core (Weeks 5-8)

#### Week 5: Order Management

**Ticket 2.1: Order Data Models**
```
Priority: P0
Estimate: 1-2 hours
Dependencies: 1.4

Description:
Define order-related data models.

Models:
```python
@dataclass
class OrderRequest:
    symbol: str
    side: Literal["buy", "sell"]
    qty: Optional[float] = None
    notional: Optional[float] = None  # Dollar amount
    type: Literal["market", "limit", "stop", "stop_limit"] = "limit"
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: Literal["day", "gtc", "ioc", "fok"] = "day"
    extended_hours: bool = False
    
@dataclass  
class Order:
    id: str
    client_order_id: str
    symbol: str
    side: str
    qty: float
    filled_qty: float
    type: str
    status: str
    submitted_at: datetime
    filled_at: Optional[datetime]
    filled_avg_price: Optional[float]
```

Claude Code Prompt:
"Create data models for orders in the AlpacaDesk trading engine. 
Include OrderRequest for submitting new orders and Order for 
tracking order state. Use Python dataclasses with proper typing."
```

**Ticket 2.2: Order Submission Service**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 2.1, 1.8, 1.19

Description:
Implement order submission with intelligent defaults.

Acceptance Criteria:
- [ ] submit_order() method handles all order types
- [ ] Default to limit orders with smart pricing
- [ ] Position sizing validation (can't exceed buying power)
- [ ] Rate limit awareness
- [ ] Returns Order object with status

Claude Code Prompt:
"Create an OrderService class for submitting orders to Alpaca. 
Support market, limit, stop, and stop-limit orders. Default to 
limit orders with price set slightly above ask (for buys) or 
below bid (for sells). Validate position sizing against buying power.
Respect rate limits."
```

**Ticket 2.3: Order Submission UI**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 2.2

Description:
Build manual order entry form.

Acceptance Criteria:
- [ ] Symbol input with autocomplete
- [ ] Buy/Sell toggle
- [ ] Order type selector
- [ ] Quantity/Dollar amount toggle
- [ ] Limit price input (when applicable)
- [ ] Estimated cost display
- [ ] Submit button with confirmation

Claude Code Prompt:
"Create an OrderEntry component for manual order submission. Include 
symbol autocomplete, buy/sell toggle, order type dropdown, quantity 
input, and limit price field. Show estimated order value. Include 
submit confirmation dialog. Style with Tailwind dark theme."
```

**Ticket 2.4: Open Orders Display**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 2.1, 1.17

Description:
Show pending orders with real-time updates.

Acceptance Criteria:
- [ ] Table of open orders
- [ ] Real-time status updates via WebSocket
- [ ] Cancel button per order
- [ ] Cancel all button
- [ ] Visual indication of partial fills

Claude Code Prompt:
"Create an OpenOrders component showing all pending orders. Update 
in real-time via WebSocket. Include cancel functionality for 
individual orders and bulk cancel. Show fill progress for 
partially filled orders."
```

**Ticket 2.5: Order History**
```
Priority: P1
Estimate: 2-3 hours
Dependencies: 2.1

Description:
Display completed order history.

Acceptance Criteria:
- [ ] Paginated list of filled/canceled orders
- [ ] Filter by symbol, date range, side
- [ ] Calculate realized P&L per trade (when possible)
- [ ] Export to CSV

Claude Code Prompt:
"Create an OrderHistory component showing completed orders. Include 
filtering by symbol and date range. Display fill price, quantity, 
and fees. Calculate realized P&L by matching buys and sells. 
Add CSV export functionality."
```

#### Week 6: Paper Trading Mode

**Ticket 2.6: Trading Mode Toggle**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.6, 1.8

Description:
Allow switching between paper and live trading.

Acceptance Criteria:
- [ ] Mode selector in settings and header
- [ ] Store credentials for both modes separately
- [ ] Clear visual indicator of current mode
- [ ] Confirmation when switching to live mode
- [ ] All API calls route to correct environment

UI:
```
┌─────────────────────────────────┐
│  Mode: [🟡 Paper ▼]              │
│        ├─ 🟡 Paper Trading       │
│        └─ 🔴 Live Trading        │
└─────────────────────────────────┘
```

Claude Code Prompt:
"Implement trading mode toggle for AlpacaDesk. Support switching 
between paper and live trading modes. Store credentials separately 
for each mode. Show prominent visual indicator of current mode 
(yellow for paper, red for live). Require confirmation when 
switching to live mode."
```

**Ticket 2.7: Paper Trading Parity Checks**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 2.6

Description:
Ensure paper trading behaves like live.

Acceptance Criteria:
- [ ] Same order validation rules
- [ ] Same position limits
- [ ] Market hours enforcement
- [ ] Simulated slippage logging
- [ ] Test suite comparing paper vs live code paths

Claude Code Prompt:
"Implement validation to ensure paper trading mode uses identical 
code paths to live trading. Add tests that verify order validation, 
position limits, and market hours are enforced the same way in both 
modes. Log simulated slippage for paper trades."
```

**Ticket 2.8: Go-Live Transition Flow**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 2.6, 2.7

Description:
Implement the paper-to-live transition with safety gates.

Acceptance Criteria:
- [ ] Review screen showing paper trading stats
- [ ] Risk acknowledgment checkboxes
- [ ] Position size limit configuration
- [ ] Typed confirmation phrase
- [ ] Audit log entry

UI: See Section 4.5 "Go-Live Transition Flow"

Claude Code Prompt:
"Create a GoLiveModal component for transitioning from paper to 
live trading. Show paper trading performance summary. Require users 
to acknowledge risks with checkboxes. Set maximum position sizes. 
Require typing 'GO LIVE' to confirm. Log the transition event."
```

#### Week 7: Bracket Orders & Risk Management

**Ticket 2.9: Bracket Order Support**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 2.2

Description:
Implement bracket orders (entry + stop loss + take profit).

Acceptance Criteria:
- [ ] submit_bracket_order() method
- [ ] Links stop loss and take profit to entry order
- [ ] Updates stops when entry fills
- [ ] Handles partial fills correctly
- [ ] Cancels related orders when one triggers

Claude Code Prompt:
"Implement bracket order support in the OrderService. A bracket 
order includes an entry order with attached stop loss and take 
profit orders. Handle the OCO (one-cancels-other) logic for 
exit orders. Support partial fills by adjusting exit order quantities."
```

**Ticket 2.10: Bracket Order UI**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 2.9, 2.3

Description:
Add bracket order options to order entry form.

Acceptance Criteria:
- [ ] Toggle for "Add Stop Loss"
- [ ] Stop loss input (price or percentage)
- [ ] Toggle for "Add Take Profit"
- [ ] Take profit input (price or percentage)
- [ ] Preview showing all three orders

Claude Code Prompt:
"Extend the OrderEntry component with bracket order options. Add 
toggles for stop loss and take profit. Allow input as price or 
percentage from entry. Show preview of all orders before submission."
```

**Ticket 2.11: Position-Level Stop Loss Management**
```
Priority: P1
Estimate: 2-3 hours
Dependencies: 2.9

Description:
Manage stops across all positions.

Acceptance Criteria:
- [ ] View all active stop orders
- [ ] Edit stop prices inline
- [ ] Bulk set stops (e.g., 5% on all positions)
- [ ] Trailing stop conversion option

Claude Code Prompt:
"Create a StopLossManager component showing all positions and their 
attached stop orders. Allow inline editing of stop prices. Add bulk 
action to set stops as percentage across all positions. Include 
option to convert to trailing stops."
```

**Ticket 2.12: Risk Guardrails**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 2.2

Description:
Implement configurable risk limits.

Acceptance Criteria:
- [ ] Max position size (% of portfolio)
- [ ] Max single order value
- [ ] Max total exposure
- [ ] Daily loss limit
- [ ] Block trades when limits exceeded

Settings:
```python
@dataclass
class RiskLimits:
    max_position_pct: float = 0.10  # 10% of portfolio
    max_order_value: float = 10000.00
    max_total_exposure_pct: float = 0.80  # 80% invested max
    daily_loss_limit_pct: float = 0.05  # Stop trading at 5% daily loss
```

Claude Code Prompt:
"Implement risk guardrails in the OrderService. Add configurable 
limits for position size, order value, total exposure, and daily 
loss. Block orders that would exceed limits with clear error messages. 
Store limits in user settings."
```

#### Week 8: Execution Quality

**Ticket 2.13: Slippage Tracking**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 2.1, 2.2

Description:
Track and report execution slippage.

Acceptance Criteria:
- [ ] Record expected vs actual fill price
- [ ] Calculate slippage per order
- [ ] Aggregate statistics (avg, max, by symbol)
- [ ] Store in local database for analysis

Claude Code Prompt:
"Implement slippage tracking in the trading engine. For each order, 
record the expected price (at submission time) and actual fill price. 
Calculate and store slippage. Aggregate statistics by symbol and 
time period. Store in SQLite for historical analysis."
```

**Ticket 2.14: Execution Quality Dashboard**
```
Priority: P1
Estimate: 2-3 hours
Dependencies: 2.13

Description:
Display execution quality metrics.

Acceptance Criteria:
- [ ] Average slippage (30 days)
- [ ] Slippage by symbol chart
- [ ] Fill rate percentage
- [ ] Recommendations for improvement

UI: See Section 3.1 "Execution Quality Dashboard"

Claude Code Prompt:
"Create an ExecutionQuality component showing trading performance 
metrics. Display average slippage, fill rate, and per-symbol analysis. 
Include recommendations when slippage is high (e.g., 'Consider limit 
orders for TSLA'). Visualize with charts."
```

**Ticket 2.15: Intelligent Order Pricing**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 2.2, 1.16

Description:
Implement smart limit order pricing.

Acceptance Criteria:
- [ ] Calculate optimal limit price based on spread
- [ ] Adjust for volatility (wider buffer when ATR high)
- [ ] Account for order size (larger = more buffer)
- [ ] Configuration options for aggressiveness

Claude Code Prompt:
"Implement intelligent limit order pricing. For buy orders, calculate 
price as: ask + (spread × buffer_multiplier). Adjust buffer based on 
ATR (higher volatility = larger buffer). Consider order size impact. 
Make aggressiveness configurable."
```

**Ticket 2.16: Local SQLite Database Setup**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 1.4

Description:
Set up local database for order history and performance tracking.

Acceptance Criteria:
- [ ] SQLite database file in user data directory
- [ ] Tables: orders, executions, daily_snapshots, strategy_runs
- [ ] Migration system for schema updates
- [ ] Backup/restore functionality

Claude Code Prompt:
"Set up SQLite database for AlpacaDesk local storage. Create tables 
for orders, executions, daily portfolio snapshots, and strategy runs. 
Use Alembic for migrations. Store database in user's AppData directory. 
Add backup and restore functions."
```

**Ticket 2.17: Multi-Broker Architecture (Preparation)**
```
Priority: P1
Estimate: 3-4 hours
Dependencies: 1.8

Description:
Refactor to support multiple brokers.

Acceptance Criteria:
- [ ] BrokerInterface abstract base class
- [ ] AlpacaBroker implements BrokerInterface
- [ ] BrokerFactory for creating broker instances
- [ ] Configuration for broker selection
- [ ] All trading code uses BrokerInterface, not Alpaca directly

Interface:
```python
class BrokerInterface(ABC):
    @abstractmethod
    def authenticate(self, credentials: dict) -> bool: ...
    @abstractmethod
    def get_account(self) -> Account: ...
    @abstractmethod
    def get_positions(self) -> List[Position]: ...
    @abstractmethod
    def submit_order(self, order: OrderRequest) -> Order: ...
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool: ...
```

Claude Code Prompt:
"Refactor the trading engine to support multiple brokers. Create 
BrokerInterface abstract base class. Refactor AlpacaClient to 
AlpacaBroker implementing this interface. Create BrokerFactory. 
Update all code to use BrokerInterface. This prepares for adding 
Interactive Brokers and Tradier in Phase 5."
```

**Ticket 2.18: Market Hours Enforcement**
```
Priority: P0
Estimate: 1-2 hours
Dependencies: 2.2

Description:
Enforce trading hours appropriately.

Acceptance Criteria:
- [ ] Check market open status before orders
- [ ] Handle pre-market and after-hours correctly
- [ ] Show countdown to market open/close
- [ ] Queue orders for market open (optional)

Claude Code Prompt:
"Implement market hours checking in the order service. Block market 
orders outside regular hours. Allow limit orders in extended hours 
only if extended_hours=True. Show market status (open, pre-market, 
after-hours, closed) in UI with countdown to next state change."
```

---

### 7.5 Phase 3: Strategy Engine (Weeks 9-12)

#### Week 9: Strategy Framework

**Ticket 3.1: Strategy Data Models**
```
Priority: P0
Estimate: 2-3 hours

Models:
```python
@dataclass
class StrategyConfig:
    id: str
    name: str
    type: str  # "momentum", "mean_reversion", "custom"
    universe: List[str]  # Symbols to evaluate
    parameters: Dict[str, Any]
    entry_conditions: List[Condition]
    exit_conditions: List[Condition]
    position_sizing: PositionSizing
    risk_management: RiskManagement
    schedule: Schedule
    is_active: bool
    is_paper: bool
    
@dataclass
class StrategyRun:
    id: str
    strategy_id: str
    timestamp: datetime
    symbols_evaluated: int
    signals_generated: int
    orders_submitted: int
    errors: List[str]
```
```

**Ticket 3.2: Strategy Engine Core**
```
Priority: P0
Estimate: 4-5 hours
Dependencies: 3.1

Description:
Build the core strategy evaluation engine.

Acceptance Criteria:
- [ ] StrategyEngine class orchestrates execution
- [ ] Loads strategy configs from storage
- [ ] Schedules evaluations based on triggers
- [ ] Evaluates conditions against market data
- [ ] Generates and submits orders
- [ ] Logs all activity

Claude Code Prompt:
"Create StrategyEngine class that orchestrates automated trading. 
Load strategy configurations, schedule evaluations based on triggers 
(time interval, market events), evaluate entry/exit conditions 
against market data, generate and submit orders via OrderService, 
and log all activity. Use asyncio for concurrent strategy evaluation."
```

**Ticket 3.3: Technical Indicator Library**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 1.10

Description:
Implement common technical indicators.

Indicators to implement:
- Moving Averages: SMA, EMA, WMA
- Momentum: RSI, MACD, Stochastic, ROC
- Volatility: Bollinger Bands, ATR, Keltner Channels
- Volume: OBV, VWAP, Volume SMA
- Trend: ADX, Aroon

Acceptance Criteria:
- [ ] IndicatorLibrary class with all indicators
- [ ] Consistent interface: indicator(data, period, **params)
- [ ] Efficient calculation using pandas/numpy
- [ ] Caching for repeated calculations
- [ ] Unit tests with known values

Claude Code Prompt:
"Create a technical indicator library for AlpacaDesk. Implement 
SMA, EMA, RSI, MACD, Bollinger Bands, ATR, and ADX. Use pandas 
for efficient calculation. Create consistent interface for all 
indicators. Include unit tests with known values from TradingView."
```

**Ticket 3.4: Condition Evaluator**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 3.3

Description:
Evaluate entry/exit conditions against data.

Acceptance Criteria:
- [ ] ConditionEvaluator class
- [ ] Supports comparison operators (>, <, ==, crosses above/below)
- [ ] Combines conditions with AND/OR logic
- [ ] Returns boolean + explanation
- [ ] Handles missing data gracefully

Claude Code Prompt:
"Create ConditionEvaluator that evaluates trading conditions against 
market data. Support operators: greater_than, less_than, equals, 
crosses_above, crosses_below. Handle AND/OR combination of conditions. 
Return result with explanation (e.g., 'RSI(14) = 28 < 30'). Handle 
missing data with appropriate defaults."
```

#### Week 10: Pre-Built Strategies

**Ticket 3.5: Momentum Breakout Strategy**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 3.2, 3.3, 3.4

Description:
Implement the first pre-built strategy.

Strategy Logic:
- Entry: Price > N-day high AND Volume > 1.5x average
- Exit: Stop loss at 5% OR Take profit at 15% OR N-day low breakdown
- Position Size: Configurable % of portfolio

Acceptance Criteria:
- [ ] MomentumBreakoutStrategy class
- [ ] Configurable parameters (lookback, volume_mult, stop, target)
- [ ] Full backtest validation
- [ ] Documentation with expected performance

Claude Code Prompt:
"Implement MomentumBreakoutStrategy for AlpacaDesk. Entry when price 
breaks above N-day high with volume confirmation. Exit on stop loss, 
take profit, or breakdown. Make all parameters configurable. Include 
detailed docstrings explaining the strategy logic."
```

**Ticket 3.6: Mean Reversion RSI Strategy**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 3.2, 3.3, 3.4

Strategy Logic:
- Entry: RSI < 30 AND Price > 200-day MA (uptrend filter)
- Exit: RSI > 70 OR Stop loss at 3%
- Position Size: Scale in (1/3 at RSI 30, 1/3 at 25, 1/3 at 20)
```

**Ticket 3.7: Dual Moving Average Strategy**
```
Priority: P0  
Estimate: 2-3 hours
Dependencies: 3.2, 3.3, 3.4

Strategy Logic:
- Entry: Fast MA crosses above Slow MA AND Price > Trend MA
- Exit: Fast MA crosses below Slow MA
- Default: 20/50/200 day MAs
```

**Ticket 3.8: Bollinger Band Mean Reversion Strategy**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 3.2, 3.3, 3.4

Strategy Logic:
- Entry: Price < Lower Band AND RSI < 40
- Exit: Price > Middle Band OR Stop loss at 5%
```

**Ticket 3.9: Relative Strength Rotation Strategy**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 3.2, 3.3, 3.4

Strategy Logic:
- Monthly evaluation
- Rank universe by 3/6/12 month momentum
- Hold top N performers
- Rebalance to equal weight
```

#### Week 11: Backtesting Engine

**Ticket 3.10: Backtest Data Manager**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 1.10

Description:
Manage historical data for backtesting.

Acceptance Criteria:
- [ ] Fetch and cache historical bars from Alpaca
- [ ] Support multiple timeframes (1min, 1hour, 1day)
- [ ] Store in local SQLite for reuse
- [ ] Data quality checks (gaps, splits)
- [ ] 5+ years of daily data available

Claude Code Prompt:
"Create BacktestDataManager to handle historical market data. Fetch 
data from Alpaca API and cache in local SQLite. Support daily and 
minute timeframes. Detect and handle data quality issues (gaps, 
splits). Implement incremental updates for efficiency."
```

**Ticket 3.11: Backtest Engine Core**
```
Priority: P0
Estimate: 4-5 hours
Dependencies: 3.2, 3.10

Description:
Event-driven backtesting engine.

Acceptance Criteria:
- [ ] BacktestEngine class
- [ ] Event loop processes bars chronologically
- [ ] Strategy receives data and generates signals
- [ ] Simulates order execution with configurable slippage
- [ ] Tracks portfolio state through time
- [ ] Generates performance metrics

Claude Code Prompt:
"Create an event-driven BacktestEngine. Process historical bars 
chronologically, feeding data to strategies, executing simulated 
trades with configurable slippage and commissions, and tracking 
portfolio value over time. Generate equity curve and performance 
statistics."
```

**Ticket 3.12: Backtest Metrics Calculator**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 3.11

Metrics to calculate:
- Total Return, CAGR
- Sharpe Ratio, Sortino Ratio
- Max Drawdown, Avg Drawdown
- Win Rate, Profit Factor
- Average Win/Loss
- Number of Trades
- Exposure Time
```

**Ticket 3.13: Backtest Results UI**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 3.11, 3.12

Description:
Display backtest results with charts and metrics.

UI: See Section 4.4 "Backtest Results UI"

Acceptance Criteria:
- [ ] Equity curve chart with benchmark
- [ ] Key metrics summary cards
- [ ] Trade list with entry/exit details
- [ ] Drawdown chart
- [ ] Monthly returns heatmap
- [ ] Export report to PDF/HTML
```

**Ticket 3.14: Backtest Configuration UI**
```
Priority: P0
Estimate: 2-3 hours
Dependencies: 3.11

Description:
UI for configuring and running backtests.

Acceptance Criteria:
- [ ] Date range selector (start/end)
- [ ] Universe selector (symbols or list)
- [ ] Initial capital input
- [ ] Slippage/commission settings
- [ ] Run button with progress indicator
- [ ] Queue multiple backtests
```

#### Week 12: Strategy Deployment

**Ticket 3.15: Strategy Management UI**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 3.2

Description:
Interface for managing deployed strategies.

Acceptance Criteria:
- [ ] List of all strategies (active/inactive)
- [ ] Deploy/pause/stop controls
- [ ] Strategy status (running, paused, error)
- [ ] Last run time and result
- [ ] Quick stats (trades, P&L)
```

**Ticket 3.16: Strategy Scheduling System**
```
Priority: P0
Estimate: 3-4 hours
Dependencies: 3.2

Description:
Schedule strategy evaluations.

Acceptance Criteria:
- [ ] Time-based triggers (every N minutes during market hours)
- [ ] Market event triggers (open, close)
- [ ] Scheduler persists across app restarts
- [ ] Handle missed evaluations gracefully
```

---

### 7.6 Phase 4: Visual Builder (Weeks 13-16)

See Section 5 for detailed UI/UX specifications.

**Tickets 4.1-4.14:** Implement each component of the visual builder:
- Canvas component with drag-drop
- Block palette
- Trigger blocks (time, price, webhook)
- Universe selector
- Condition builder
- Action blocks
- Flow control blocks
- Connection lines
- Validation system
- Auto-generated summary
- Template system
- Export to code (Pro)
- Import/share strategies

---

### 7.7 Phase 5: Polish & Launch (Weeks 17-20)

**Tickets 5.1-5.12:** Final launch preparation:
- Interactive Brokers integration
- Tradier integration
- Onboarding flow implementation
- Help system and tooltips
- Performance optimization
- Error tracking integration
- Analytics integration
- Beta testing program
- Documentation site
- Marketing site
- Payment integration (Stripe)
- Launch checklist

---

## 8. Technical Architecture

### 8.1 Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **UI Framework** | Electron + React | Cross-platform potential, rich ecosystem, rapid development |
| **Language** | TypeScript (UI), Python (strategy engine) | TS for UI safety; Python for trading logic (match Alpaca SDK) |
| **Local Database** | SQLite | Zero-config, reliable, adequate for single-user data |
| **Charting** | Lightweight-charts + TradingView embed | Best of both worlds |
| **Credential Storage** | Windows Credential Manager (keytar) | OS-level encryption |
| **IPC** | Electron IPC + local HTTP | UI ↔ Python engine communication |
| **Packaging** | Electron Builder | Single .exe installer |

### 8.2 File Structure

```
alpacadesk/
├── package.json
├── electron/
│   ├── main.ts              # Electron main process
│   ├── preload.ts           # IPC bridge
│   └── pythonBridge.ts      # Python process manager
├── src/                     # React frontend
│   ├── main.tsx
│   ├── App.tsx
│   ├── components/
│   │   ├── common/          # Shared UI components
│   │   ├── dashboard/       # Dashboard components
│   │   ├── strategies/      # Strategy list/management
│   │   ├── builder/         # Visual strategy builder
│   │   ├── backtest/        # Backtest UI
│   │   └── settings/        # Settings pages
│   ├── hooks/               # Custom React hooks
│   ├── services/            # API service layer
│   ├── store/               # State management (Zustand)
│   └── types/               # TypeScript types
├── engine/                  # Python trading engine
│   ├── pyproject.toml
│   └── src/alpacadesk_engine/
│       ├── main.py          # FastAPI entry point
│       ├── api/             # HTTP routes
│       ├── brokers/         # Broker implementations
│       │   ├── interface.py # BrokerInterface ABC
│       │   ├── alpaca.py    # Alpaca implementation
│       │   ├── ibkr.py      # Interactive Brokers (Phase 5)
│       │   └── tradier.py   # Tradier (Phase 5)
│       ├── strategies/      # Strategy implementations
│       │   ├── base.py      # BaseStrategy ABC
│       │   ├── momentum.py
│       │   ├── mean_reversion.py
│       │   └── custom.py    # Custom strategy runner
│       ├── backtest/        # Backtesting engine
│       ├── indicators/      # Technical indicators
│       ├── services/        # Business logic services
│       └── utils/           # Utilities
└── resources/               # Static assets
```

---

## 9. Risk Assessment

### 9.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Alpaca API changes break integration | Medium | High | Abstract broker layer; monitor changelog; test suite |
| Rate limiting causes missed trades | Medium | Medium | WebSocket-first; intelligent caching; user education |
| Electron performance issues | Low | Medium | Profile aggressively; offload to Python; lazy loading |
| Claude Code hits complexity ceiling | Medium | Medium | Break into smaller tickets; have fallback plan for manual coding |
| Windows Credential Manager issues | Low | High | Fallback to encrypted file storage; test across Windows versions |

### 9.2 Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Low conversion rate (<5%) | Medium | High | Aggressive A/B testing; user interviews; feature iteration |
| High support costs from non-technical users | Medium | Medium | Extensive self-serve docs; video tutorials; community forums |
| Competitor launches similar product | Medium | Medium | First-mover advantage; rapid iteration; community lock-in |
| Regulatory scrutiny | Low | High | Clear disclaimers; consult fintech lawyer; no personalized advice |

---

## 10. Success Metrics & KPIs

### 10.1 Development Metrics (Claude Code Specific)

| Metric | Target |
|--------|--------|
| Tickets completed per week | 4-5 |
| First-attempt success rate | 70%+ |
| Rework tickets | <20% |
| Test coverage | 60%+ |

### 10.2 Product Metrics (Post-Launch)

| Metric | 6-Month Target |
|--------|----------------|
| MAU | 5,000 |
| Paid Conversion | 8% |
| MRR | $25,000 |
| NPS | 40+ |
| Churn | <5%/month |

---

## 11. Appendix

### A. Claude Code Session Template

Use this template when starting each ticket:

```
TICKET: [Ticket ID and Title]

CONTEXT:
- AlpacaDesk is a native Windows Electron + Python trading app
- This ticket is part of Phase [X]: [Phase Name]
- Dependencies completed: [List]

REQUIREMENTS:
[Copy acceptance criteria from ticket]

EXISTING CODE REFERENCE:
[Paste relevant existing code or file structure]

CONSTRAINTS:
- Use TypeScript for frontend, Python for backend
- Follow existing code style
- Include error handling
- Add basic tests where appropriate

OUTPUT:
Please provide complete, working code for this ticket.
```

### B. Testing Strategy

| Test Type | Coverage Target | Tools |
|-----------|-----------------|-------|
| Unit Tests | 60% | pytest (Python), Jest (TypeScript) |
| Integration Tests | Key flows | pytest + mock APIs |
| E2E Tests | Critical paths | Playwright |
| Manual Testing | All features | Checklist before release |

### C. Definition of Done

A ticket is complete when:
- [ ] Code compiles without errors
- [ ] Acceptance criteria met
- [ ] Basic error handling included
- [ ] Works in both paper and live modes (if applicable)
- [ ] No console errors in dev tools
- [ ] Tested manually in development build

---

*Document Version: 1.1*
*Last Updated: January 2026*
*Status: Approved for Development*
