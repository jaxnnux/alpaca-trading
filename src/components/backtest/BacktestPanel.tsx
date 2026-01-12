import React, { useState } from 'react';
import { backtestService } from '../../services/backtestService';
import { BacktestRequest, BacktestResult } from '../../types';
import EquityChart from '../charts/EquityChart';
import './BacktestPanel.css';

const BacktestPanel: React.FC = () => {
  const [strategyType, setStrategyType] = useState('momentum_breakout');
  const [symbols, setSymbols] = useState('SPY');
  const [startDate, setStartDate] = useState(() => {
    const date = new Date();
    date.setFullYear(date.getFullYear() - 1);
    return date.toISOString().split('T')[0];
  });
  const [endDate, setEndDate] = useState(() => {
    return new Date().toISOString().split('T')[0];
  });
  const [initialCapital, setInitialCapital] = useState(100000);

  const [result, setResult] = useState<BacktestResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRunBacktest = async () => {
    setError('');
    setLoading(true);
    setResult(null);

    try {
      const symbolsArray = symbols.split(',').map((s) => s.trim());

      const request: BacktestRequest = {
        strategyType,
        symbols: symbolsArray,
        parameters: getDefaultParameters(strategyType),
        startDate: new Date(startDate).toISOString(),
        endDate: new Date(endDate).toISOString(),
        initialCapital,
      };

      const backtestResult = await backtestService.runBacktest(request);
      setResult(backtestResult);
    } catch (err: any) {
      setError(err.message || 'Backtest failed');
    } finally {
      setLoading(false);
    }
  };

  const getDefaultParameters = (type: string) => {
    switch (type) {
      case 'momentum_breakout':
        return {
          lookback_period: 20,
          volume_multiplier: 1.5,
          position_size_pct: 10,
          stop_loss_pct: 5,
          take_profit_pct: 15,
          max_positions: 5,
        };
      case 'mean_reversion_rsi':
        return {
          rsi_period: 14,
          rsi_oversold: 30,
          rsi_overbought: 70,
          ma_period: 200,
          position_size_pct: 10,
        };
      default:
        return {};
    }
  };

  return (
    <div className="backtest-panel">
      <h2>Backtest Engine</h2>
      <p className="subtitle">Test your strategies against historical data</p>

      <div className="backtest-config card">
        <div className="card-header">Configuration</div>
        <div className="card-body">
          <div className="config-grid">
            <div className="form-group">
              <label>Strategy Type</label>
              <select
                className="input"
                value={strategyType}
                onChange={(e) => setStrategyType(e.target.value)}
              >
                <option value="momentum_breakout">Momentum Breakout</option>
                <option value="mean_reversion_rsi">Mean Reversion RSI</option>
              </select>
            </div>

            <div className="form-group">
              <label>Symbols (comma-separated)</label>
              <input
                type="text"
                className="input"
                value={symbols}
                onChange={(e) => setSymbols(e.target.value)}
                placeholder="SPY, QQQ, IWM"
              />
            </div>

            <div className="form-group">
              <label>Start Date</label>
              <input
                type="date"
                className="input"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>End Date</label>
              <input
                type="date"
                className="input"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Initial Capital</label>
              <input
                type="number"
                className="input"
                value={initialCapital}
                onChange={(e) => setInitialCapital(Number(e.target.value))}
              />
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            className="btn btn-primary btn-large"
            onClick={handleRunBacktest}
            disabled={loading}
          >
            {loading ? 'Running Backtest...' : 'Run Backtest'}
          </button>
        </div>
      </div>

      {result && (
        <div className="backtest-results">
          <div className="metrics-grid">
            <div className="metric-card card">
              <div className="metric-label">Total Return</div>
              <div className={`metric-value ${result.totalReturn >= 0 ? 'positive' : 'negative'}`}>
                {result.totalReturn.toFixed(2)}%
              </div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Buy & Hold</div>
              <div className={`metric-value ${result.buyAndHoldReturn >= 0 ? 'positive' : 'negative'}`}>
                {result.buyAndHoldReturn.toFixed(2)}%
              </div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Max Drawdown</div>
              <div className="metric-value negative">{result.maxDrawdown.toFixed(2)}%</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Sharpe Ratio</div>
              <div className="metric-value">{result.sharpeRatio.toFixed(2)}</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Win Rate</div>
              <div className="metric-value">{result.winRate.toFixed(1)}%</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Total Trades</div>
              <div className="metric-value">{result.totalTrades}</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Winning Trades</div>
              <div className="metric-value positive">{result.winningTrades}</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Losing Trades</div>
              <div className="metric-value negative">{result.losingTrades}</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Avg Win</div>
              <div className="metric-value positive">${result.avgWin.toFixed(2)}</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Avg Loss</div>
              <div className="metric-value negative">${result.avgLoss.toFixed(2)}</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Avg Duration</div>
              <div className="metric-value">{result.avgTradeDurationDays.toFixed(1)} days</div>
            </div>

            <div className="metric-card card">
              <div className="metric-label">Max Streak</div>
              <div className="metric-value">
                {result.maxConsecutiveWins}W / {result.maxConsecutiveLosses}L
              </div>
            </div>
          </div>

          <div className="equity-chart-container card">
            <div className="card-header">Equity Curve</div>
            <div className="card-body">
              <EquityChart data={result.equityCurve} height={400} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BacktestPanel;
