import React, { useState, useEffect } from 'react';
import './ExecutionQuality.css';

interface ExecutionMetrics {
  totalOrders: number;
  avgSlippage: number;
  fillRate: number;
  unfilled: number;
  avgFillTime: number;
  recentOrders: OrderExecution[];
}

interface OrderExecution {
  symbol: string;
  side: string;
  orderType: string;
  expectedPrice: number;
  actualPrice: number;
  slippagePct: number;
  fillTime: number;
  timestamp: string;
}

const ExecutionQuality: React.FC = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [metrics, setMetrics] = useState<ExecutionMetrics>({
    totalOrders: 47,
    avgSlippage: 0.03,
    fillRate: 94.2,
    unfilled: 3,
    avgFillTime: 0.8,
    recentOrders: [
      {
        symbol: 'AAPL',
        side: 'buy',
        orderType: 'limit',
        expectedPrice: 185.50,
        actualPrice: 185.52,
        slippagePct: 0.01,
        fillTime: 0.5,
        timestamp: '2026-01-12T10:30:00Z',
      },
      {
        symbol: 'MSFT',
        side: 'sell',
        orderType: 'market',
        expectedPrice: 420.00,
        actualPrice: 419.85,
        slippagePct: -0.04,
        fillTime: 0.2,
        timestamp: '2026-01-12T11:15:00Z',
      },
      {
        symbol: 'TSLA',
        side: 'buy',
        orderType: 'market',
        expectedPrice: 245.00,
        actualPrice: 245.30,
        slippagePct: 0.12,
        fillTime: 0.3,
        timestamp: '2026-01-12T14:20:00Z',
      },
    ],
  });

  const getSlippageColor = (slippage: number) => {
    if (Math.abs(slippage) < 0.05) return 'good';
    if (Math.abs(slippage) < 0.15) return 'warning';
    return 'poor';
  };

  const marketOrderAvg = 0.15; // Benchmark for market orders

  return (
    <div className="execution-quality">
      <div className="quality-header">
        <div>
          <h2>📊 Execution Quality Dashboard</h2>
          <p>Track and optimize your order execution performance</p>
        </div>
        <div className="time-range-selector">
          <button
            className={`time-btn ${timeRange === '1d' ? 'active' : ''}`}
            onClick={() => setTimeRange('1d')}
          >
            1D
          </button>
          <button
            className={`time-btn ${timeRange === '7d' ? 'active' : ''}`}
            onClick={() => setTimeRange('7d')}
          >
            7D
          </button>
          <button
            className={`time-btn ${timeRange === '30d' ? 'active' : ''}`}
            onClick={() => setTimeRange('30d')}
          >
            30D
          </button>
        </div>
      </div>

      <div className="metrics-summary">
        <div className="metric-box card">
          <div className="metric-icon">📈</div>
          <div className="metric-content">
            <div className="metric-label">Orders Executed</div>
            <div className="metric-value">{metrics.totalOrders}</div>
          </div>
        </div>

        <div className="metric-box card">
          <div className="metric-icon">💹</div>
          <div className="metric-content">
            <div className="metric-label">Avg Slippage</div>
            <div className={`metric-value ${getSlippageColor(metrics.avgSlippage)}`}>
              {metrics.avgSlippage.toFixed(3)}%
            </div>
            <div className="metric-comparison">
              vs. {marketOrderAvg.toFixed(2)}% market order avg
            </div>
          </div>
        </div>

        <div className="metric-box card">
          <div className="metric-icon">✅</div>
          <div className="metric-content">
            <div className="metric-label">Fill Rate</div>
            <div className="metric-value">{metrics.fillRate.toFixed(1)}%</div>
          </div>
        </div>

        <div className="metric-box card">
          <div className="metric-icon">⏱️</div>
          <div className="metric-content">
            <div className="metric-label">Avg Fill Time</div>
            <div className="metric-value">{metrics.avgFillTime.toFixed(1)}s</div>
          </div>
        </div>
      </div>

      <div className="insights card">
        <div className="card-header">💡 Insights & Recommendations</div>
        <div className="card-body">
          {metrics.avgSlippage < 0.05 ? (
            <div className="insight good">
              <span className="insight-icon">✅</span>
              <div>
                <strong>Excellent execution quality!</strong>
                <p>Your average slippage of {metrics.avgSlippage.toFixed(3)}% is well below the market order average.</p>
              </div>
            </div>
          ) : (
            <div className="insight warning">
              <span className="insight-icon">⚠️</span>
              <div>
                <strong>Slippage detected</strong>
                <p>Your TSLA orders show 0.12% avg slippage. Consider using limit orders with 0.1% buffer for this volatile ticker.</p>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="recent-orders card">
        <div className="card-header">Recent Executions</div>
        <div className="card-body">
          <table className="orders-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Symbol</th>
                <th>Side</th>
                <th>Type</th>
                <th>Expected</th>
                <th>Actual</th>
                <th>Slippage</th>
                <th>Fill Time</th>
              </tr>
            </thead>
            <tbody>
              {metrics.recentOrders.map((order, index) => (
                <tr key={index}>
                  <td>{new Date(order.timestamp).toLocaleTimeString()}</td>
                  <td><strong>{order.symbol}</strong></td>
                  <td className={order.side === 'buy' ? 'buy-side' : 'sell-side'}>
                    {order.side.toUpperCase()}
                  </td>
                  <td>{order.orderType}</td>
                  <td>${order.expectedPrice.toFixed(2)}</td>
                  <td>${order.actualPrice.toFixed(2)}</td>
                  <td className={`slippage-${getSlippageColor(order.slippagePct)}`}>
                    {order.slippagePct > 0 ? '+' : ''}{order.slippagePct.toFixed(3)}%
                  </td>
                  <td>{order.fillTime.toFixed(1)}s</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="optimization-tips card">
        <div className="card-header">🎯 Optimization Tips</div>
        <div className="card-body">
          <ul className="tips-list">
            <li>
              <strong>Use Limit Orders:</strong> Reduces slippage by 60-80% vs market orders
            </li>
            <li>
              <strong>Avoid Peak Hours:</strong> First and last 15 minutes have higher volatility
            </li>
            <li>
              <strong>Adaptive Pricing:</strong> Adjust limit prices based on volatility (ATR)
            </li>
            <li>
              <strong>Monitor by Symbol:</strong> Track which stocks have consistent slippage issues
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ExecutionQuality;
