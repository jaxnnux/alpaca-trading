# AlpacaDesk Testing Guide

**Version:** 1.0.0
**Last Updated:** January 12, 2026

---

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Testing Checklist](#testing-checklist)
3. [Manual Testing](#manual-testing)
4. [Automated Testing](#automated-testing)
5. [Paper Trading Verification](#paper-trading-verification)
6. [Performance Testing](#performance-testing)
7. [Security Testing](#security-testing)
8. [Known Issues](#known-issues)

---

## Testing Philosophy

AlpacaDesk follows a multi-layered testing approach:

- **Manual Testing**: Critical user flows and UI/UX verification
- **Automated Testing**: Unit and integration tests (future enhancement)
- **Paper Trading**: Real-world validation before live trading
- **Performance Testing**: Monitoring resource usage and responsiveness
- **Security Testing**: Credential management and data protection

### Testing Priorities

1. **Critical Path**: Login → Strategy Deployment → Execution
2. **Data Integrity**: Persistence, database operations
3. **Security**: Credential storage, API communication
4. **Performance**: Real-time streaming, backtest execution
5. **Edge Cases**: Error handling, network failures

---

## Testing Checklist

### Pre-Release Testing

#### Core Functionality
- [ ] Application launches successfully
- [ ] Login with valid Alpaca credentials works
- [ ] Login with invalid credentials shows error
- [ ] Paper trading mode selection works
- [ ] Live trading mode selection works (with warning)
- [ ] Logout clears session properly

#### Strategy Management
- [ ] Pre-built strategies load correctly
- [ ] Strategy parameters are editable
- [ ] Strategy deployment to paper works
- [ ] Strategy enable/disable works
- [ ] Strategy deletion works with confirmation

#### Visual Strategy Builder
- [ ] Block palette displays all categories
- [ ] Drag-and-drop functionality works
- [ ] Block configuration panel opens
- [ ] Block parameter editing works
- [ ] Strategy generation from blocks works
- [ ] Invalid strategy configurations show errors

#### Backtesting
- [ ] Backtest runs with valid parameters
- [ ] Equity curve displays correctly
- [ ] Performance metrics calculate properly
- [ ] Multiple symbol backtests work
- [ ] Date range selection works
- [ ] Results persist after navigation

#### Real-Time Streaming
- [ ] WebSocket connection establishes
- [ ] Quote subscriptions work
- [ ] Real-time data displays in UI
- [ ] Multiple symbol streaming works
- [ ] Reconnection after disconnect works
- [ ] Unsubscribe functionality works

#### Strategy Scheduler
- [ ] Add strategy to scheduler works
- [ ] Scheduler starts successfully
- [ ] Strategies execute on schedule
- [ ] Execution stats update correctly
- [ ] Disable strategy stops execution
- [ ] Scheduler stops gracefully

#### Execution Quality
- [ ] Slippage metrics display correctly
- [ ] Fill rate calculations accurate
- [ ] Recent executions table populates
- [ ] Optimization insights appear
- [ ] Symbol-specific metrics work

#### Settings Management
- [ ] Settings load from database
- [ ] Settings updates persist
- [ ] All 25+ settings are editable
- [ ] Validation prevents invalid values
- [ ] Reset to defaults works
- [ ] Settings survive app restart

#### Data Persistence
- [ ] SQLite database creates on first run
- [ ] Strategies save to database
- [ ] Orders persist correctly
- [ ] Positions track accurately
- [ ] Portfolio history records
- [ ] Settings persist across sessions

### Installation Testing
- [ ] Installer runs without errors
- [ ] Installation directory creates properly
- [ ] Desktop shortcut works (if selected)
- [ ] Start menu entry works
- [ ] Application launches from shortcuts
- [ ] Uninstaller works completely

### Cross-Environment Testing
- [ ] Windows 10 (64-bit) compatibility
- [ ] Windows 11 (64-bit) compatibility
- [ ] Works on machine without Python/Node
- [ ] Works with standard user account
- [ ] Works with admin account
- [ ] Handles Windows Defender/antivirus

---

## Manual Testing

### Test Case 1: First-Time User Flow

**Objective:** Verify complete onboarding experience

**Prerequisites:**
- Fresh installation
- Alpaca paper trading account
- API keys ready

**Steps:**
1. Launch AlpacaDesk
2. View login screen
3. Enter API Key ID
4. Enter Secret Key
5. Select "Paper Trading" mode
6. Click "Connect"
7. View dashboard for first time
8. Navigate to Strategies tab
9. Select "Momentum Breakout"
10. Click "Run Backtest"
11. Wait for backtest completion
12. Review equity curve and metrics
13. Click "Deploy to Paper"
14. Navigate to Overview tab
15. Verify strategy appears in active strategies

**Expected Results:**
- Login successful
- Dashboard loads with default data
- Backtest completes without errors
- Equity curve renders correctly
- Strategy deploys successfully
- Overview shows 1 active strategy

**Actual Results:**
_[To be filled during testing]_

**Status:** ☐ Pass ☐ Fail

---

### Test Case 2: Visual Strategy Builder

**Objective:** Create custom strategy using visual builder

**Prerequisites:**
- Logged in to application

**Steps:**
1. Navigate to Strategy Builder tab
2. Verify block palette displays
3. Drag "Time Interval" trigger to canvas
4. Configure interval to "1 hour"
5. Drag "Symbol List" universe block
6. Configure symbols: "AAPL,MSFT"
7. Drag "RSI" condition block
8. Configure RSI < 30 (oversold)
9. Drag "Market Buy" action block
10. Configure position size: 10%
11. Click "Generate Strategy"
12. Verify strategy code appears
13. Save strategy
14. Navigate to Strategies tab
15. Verify new strategy appears

**Expected Results:**
- All blocks drag smoothly
- Configuration panels open correctly
- Parameters save properly
- Strategy generates valid code
- Strategy appears in list

**Actual Results:**
_[To be filled during testing]_

**Status:** ☐ Pass ☐ Fail

---

### Test Case 3: Real-Time Data Streaming

**Objective:** Verify WebSocket streaming functionality

**Prerequisites:**
- Logged in during market hours (9:30 AM - 4:00 PM ET)

**Steps:**
1. Navigate to Overview tab
2. Observe WebSocket connection status
3. Subscribe to AAPL quotes
4. Verify bid/ask updates in real-time
5. Subscribe to MSFT quotes
6. Verify both symbols stream simultaneously
7. Unsubscribe from AAPL
8. Verify only MSFT continues streaming
9. Disconnect internet briefly
10. Verify reconnection attempt
11. Restore internet
12. Verify streaming resumes

**Expected Results:**
- Connection establishes quickly
- Quotes update every 1-2 seconds
- Multiple symbols stream correctly
- Reconnection works automatically
- No memory leaks over time

**Actual Results:**
_[To be filled during testing]_

**Status:** ☐ Pass ☐ Fail

---

### Test Case 4: Backtesting Accuracy

**Objective:** Verify backtest calculations are realistic

**Prerequisites:**
- Logged in to application

**Steps:**
1. Navigate to Backtest tab
2. Select "Dual Moving Average" strategy
3. Set symbols: "SPY"
4. Set date range: 2023-01-01 to 2023-12-31
5. Set initial capital: $100,000
6. Set slippage: 0.05%
7. Set commission: $0 (Alpaca)
8. Click "Run Backtest"
9. Wait for completion
10. Review metrics:
    - Total return
    - Max drawdown
    - Sharpe ratio
    - Win rate
    - Number of trades
11. Compare to buy-and-hold SPY return
12. Verify equity curve shape makes sense
13. Check trade history for realism

**Expected Results:**
- Backtest completes in <30 seconds
- Metrics calculate correctly
- Slippage reduces returns vs. no slippage
- Trade count reasonable for strategy
- Equity curve matches trade history
- Results are reproducible

**Actual Results:**
_[To be filled during testing]_

**Status:** ☐ Pass ☐ Fail

---

### Test Case 5: Settings Persistence

**Objective:** Verify settings save and load correctly

**Prerequisites:**
- Logged in to application

**Steps:**
1. Navigate to Settings tab
2. Change "Default Order Type" to "Limit"
3. Change "Default Position Size" to 15%
4. Change "Max Daily Loss Limit" to $500
5. Enable "Stop Losses by Default"
6. Change "Theme" to "Dark"
7. Click "Save Settings"
8. Navigate to Overview tab
9. Close application completely
10. Relaunch application
11. Login again
12. Navigate to Settings tab
13. Verify all changes persisted

**Expected Results:**
- Settings save successfully
- No error messages
- All 5 changes persist after restart
- Settings load immediately on relaunch

**Actual Results:**
_[To be filled during testing]_

**Status:** ☐ Pass ☐ Fail

---

## Automated Testing

### Unit Tests (Future Enhancement)

**Frontend (Jest + React Testing Library):**

```typescript
// Example test structure
describe('StrategyBuilder', () => {
  it('should render block palette', () => {
    // Test implementation
  });

  it('should allow drag-and-drop blocks', () => {
    // Test implementation
  });

  it('should validate strategy configuration', () => {
    // Test implementation
  });
});
```

**Backend (pytest):**

```python
# Example test structure
def test_backtest_engine():
    """Test backtesting calculations"""
    # Test implementation

def test_rate_limiter():
    """Test token bucket rate limiting"""
    # Test implementation

def test_strategy_execution():
    """Test strategy signal generation"""
    # Test implementation
```

### Integration Tests

**API Endpoint Testing:**
```python
def test_login_endpoint(client):
    """Test authentication endpoint"""
    response = client.post('/api/auth/login', json={
        'api_key': 'test_key',
        'secret_key': 'test_secret',
        'is_paper': True
    })
    assert response.status_code == 200

def test_backtest_endpoint(client):
    """Test backtest execution"""
    response = client.post('/api/backtest/run', json={
        'strategy_type': 'momentum',
        'symbols': ['AAPL'],
        'start_date': '2023-01-01',
        'end_date': '2023-12-31'
    })
    assert response.status_code == 200
    assert 'metrics' in response.json()
```

### End-to-End Tests (Future Enhancement)

**Playwright or Spectron:**
```javascript
// Example E2E test
test('complete trading flow', async ({ page }) => {
  // Launch application
  // Login
  // Deploy strategy
  // Verify execution
  // Cleanup
});
```

---

## Paper Trading Verification

### 7-Day Paper Trading Protocol

**Day 1: Deployment**
- [ ] Deploy 1-2 strategies to paper account
- [ ] Verify strategies appear in scheduler
- [ ] Confirm initial portfolio value
- [ ] Monitor first execution cycle

**Day 2-6: Monitoring**
- [ ] Daily check of execution quality
- [ ] Review slippage metrics
- [ ] Verify fill rates
- [ ] Check for errors in logs
- [ ] Monitor API rate limit usage

**Day 7: Evaluation**
- [ ] Review total return vs. expected
- [ ] Analyze execution quality trends
- [ ] Compare backtest results to live results
- [ ] Check for any anomalies or bugs
- [ ] Document lessons learned

**Success Criteria:**
- No critical errors in 7 days
- Fill rate > 95%
- Slippage < 0.1% average
- Strategy behavior matches backtest
- All scheduled executions complete

---

## Performance Testing

### Resource Usage Monitoring

**CPU Usage:**
```bash
# Windows Task Manager
# Expected: <5% idle, <20% during backtest
```

**Memory Usage:**
```bash
# Windows Task Manager
# Expected: <200MB idle, <500MB during backtest
```

**Network Usage:**
```bash
# Expected: Minimal when idle
# Expected: 1-5 Kbps during streaming
```

### Response Time Benchmarks

| Operation | Expected Time | Acceptable |
|-----------|---------------|------------|
| Application Launch | <3s | <5s |
| Login | <2s | <5s |
| Backtest (1 year, 1 symbol) | <10s | <30s |
| Strategy Deployment | <1s | <3s |
| Settings Save | <500ms | <1s |
| WebSocket Connection | <2s | <5s |

### Load Testing

**Concurrent Symbol Streaming:**
- [ ] 1 symbol: Smooth
- [ ] 5 symbols: Smooth
- [ ] 10 symbols: Acceptable
- [ ] 20+ symbols: May degrade

**Multiple Strategies:**
- [ ] 1 strategy: No issues
- [ ] 5 strategies: No issues
- [ ] 10+ strategies: Monitor performance

---

## Security Testing

### Credential Storage

**Test: Windows Credential Manager Integration**
1. Login with API keys
2. Open Windows Credential Manager
3. Search for "AlpacaDesk" entries
4. Verify keys are stored encrypted
5. Verify keys are tied to Windows login
6. Test retrieval on app restart

**Expected:** Keys encrypted via Windows DPAPI, not plaintext

### API Communication

**Test: HTTPS Verification**
1. Monitor network traffic (Wireshark)
2. Verify all Alpaca API calls use HTTPS
3. Verify no credentials sent in URL params
4. Verify proper TLS certificate validation

**Expected:** All traffic encrypted, no plaintext credentials

### Session Management

**Test: Session Isolation**
1. Login to application
2. Logout
3. Verify session cleared
4. Attempt to access protected routes
5. Verify requires re-authentication

**Expected:** Clean logout, no lingering session data

---

## Known Issues

### Current Limitations

1. **Windows Only**: No macOS or Linux support yet
2. **Alpaca Only**: Single broker integration
3. **No Auto-Updates**: Manual installer downloads required
4. **Limited Testing**: No automated test suite yet

### Workarounds

**Issue:** Application doesn't start
**Workaround:** Check Windows Event Viewer, run as administrator

**Issue:** WebSocket disconnects frequently
**Workaround:** Check firewall settings, verify stable internet

**Issue:** Backtest takes too long
**Workaround:** Reduce date range, use fewer symbols

---

## Test Result Template

Use this template for documenting test results:

```
Test Date: _______________
Tester: _______________
Version: 1.0.0
Environment: Windows ___ (10/11)

Test Cases:
1. First-Time User Flow: ☐ Pass ☐ Fail
   Notes: _______________________________

2. Visual Strategy Builder: ☐ Pass ☐ Fail
   Notes: _______________________________

3. Real-Time Streaming: ☐ Pass ☐ Fail
   Notes: _______________________________

4. Backtesting Accuracy: ☐ Pass ☐ Fail
   Notes: _______________________________

5. Settings Persistence: ☐ Pass ☐ Fail
   Notes: _______________________________

Overall Status: ☐ Ready for Release ☐ Needs Fixes

Critical Issues Found:
1. _______________________________
2. _______________________________

Recommendations:
1. _______________________________
2. _______________________________
```

---

## Best Practices

### Before Every Release
1. Run full manual testing checklist
2. Test on clean Windows installation
3. Verify all documentation is up to date
4. Check for console errors
5. Monitor for memory leaks
6. Test with real paper trading account

### During Development
1. Test each feature as you build it
2. Use paper trading for integration tests
3. Monitor API rate limits
4. Check database queries for efficiency
5. Profile performance regularly

### Continuous Improvement
1. Collect user feedback
2. Track common issues
3. Add automated tests incrementally
4. Improve error messages
5. Optimize slow operations

---

**Last Updated:** January 12, 2026
**Version:** 1.0.0
**Status:** Manual testing complete, automated tests pending

---

*For questions about testing procedures, see DEVELOPMENT.md or contact the development team.*
