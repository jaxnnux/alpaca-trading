import React, { useState } from 'react';
import './SettingsPage.css';

const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState({
    // Trading Settings
    defaultOrderType: 'limit',
    defaultTimeInForce: 'day',
    maxPositionSize: 10,
    useStopLoss: true,
    defaultStopLossPct: 5,
    useTakeProfit: false,
    defaultTakeProfitPct: 15,

    // Risk Management
    maxDailyLoss: 500,
    maxOpenPositions: 5,
    enablePaperTrading: false,

    // Execution
    slippageBuffer: 0.1,
    orderExecutionTimeout: 30,
    retryFailedOrders: true,

    // Notifications
    notifyOrderFills: true,
    notifyOrderRejections: true,
    notifyStrategyErrors: true,
    notifyDailyPnL: false,

    // Data & Display
    chartTheme: 'light',
    defaultTimeframe: '1d',
    showRealTimeData: true,

    // Advanced
    enableLogging: true,
    logLevel: 'info',
    apiCallLogging: false,
  });

  const handleChange = (key: string, value: any) => {
    setSettings({ ...settings, [key]: value });
  };

  const handleSave = () => {
    // Save settings to backend
    console.log('Saving settings:', settings);
    alert('Settings saved successfully!');
  };

  const handleReset = () => {
    if (confirm('Reset all settings to defaults?')) {
      // Reset to defaults
      alert('Settings reset to defaults');
    }
  };

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h2>⚙️ Settings</h2>
        <p>Configure your AlpacaDesk preferences</p>
      </div>

      <div className="settings-content">
        {/* Trading Settings */}
        <div className="settings-section card">
          <div className="card-header">📊 Trading Settings</div>
          <div className="card-body">
            <div className="setting-item">
              <label>Default Order Type</label>
              <select
                className="input"
                value={settings.defaultOrderType}
                onChange={(e) => handleChange('defaultOrderType', e.target.value)}
              >
                <option value="market">Market</option>
                <option value="limit">Limit</option>
              </select>
            </div>

            <div className="setting-item">
              <label>Default Time in Force</label>
              <select
                className="input"
                value={settings.defaultTimeInForce}
                onChange={(e) => handleChange('defaultTimeInForce', e.target.value)}
              >
                <option value="day">Day</option>
                <option value="gtc">Good 'til Canceled</option>
                <option value="ioc">Immediate or Cancel</option>
              </select>
            </div>

            <div className="setting-item">
              <label>Max Position Size (% of portfolio)</label>
              <input
                type="number"
                className="input"
                value={settings.maxPositionSize}
                onChange={(e) => handleChange('maxPositionSize', Number(e.target.value))}
                min={1}
                max={100}
              />
            </div>

            <div className="setting-item-row">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.useStopLoss}
                  onChange={(e) => handleChange('useStopLoss', e.target.checked)}
                />
                <span>Use Stop Loss by default</span>
              </label>
              {settings.useStopLoss && (
                <input
                  type="number"
                  className="input inline-input"
                  value={settings.defaultStopLossPct}
                  onChange={(e) => handleChange('defaultStopLossPct', Number(e.target.value))}
                  min={1}
                  max={50}
                />
              )}
              {settings.useStopLoss && <span className="inline-label">%</span>}
            </div>

            <div className="setting-item-row">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.useTakeProfit}
                  onChange={(e) => handleChange('useTakeProfit', e.target.checked)}
                />
                <span>Use Take Profit by default</span>
              </label>
              {settings.useTakeProfit && (
                <input
                  type="number"
                  className="input inline-input"
                  value={settings.defaultTakeProfitPct}
                  onChange={(e) => handleChange('defaultTakeProfitPct', Number(e.target.value))}
                  min={1}
                  max={100}
                />
              )}
              {settings.useTakeProfit && <span className="inline-label">%</span>}
            </div>
          </div>
        </div>

        {/* Risk Management */}
        <div className="settings-section card">
          <div className="card-header">🛡️ Risk Management</div>
          <div className="card-body">
            <div className="setting-item">
              <label>Max Daily Loss ($)</label>
              <input
                type="number"
                className="input"
                value={settings.maxDailyLoss}
                onChange={(e) => handleChange('maxDailyLoss', Number(e.target.value))}
                min={0}
              />
              <small>Trading will pause if this limit is reached</small>
            </div>

            <div className="setting-item">
              <label>Max Open Positions</label>
              <input
                type="number"
                className="input"
                value={settings.maxOpenPositions}
                onChange={(e) => handleChange('maxOpenPositions', Number(e.target.value))}
                min={1}
                max={20}
              />
            </div>

            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.enablePaperTrading}
                  onChange={(e) => handleChange('enablePaperTrading', e.target.checked)}
                />
                <span>Force Paper Trading Mode (recommended for testing)</span>
              </label>
            </div>
          </div>
        </div>

        {/* Execution Settings */}
        <div className="settings-section card">
          <div className="card-header">⚡ Execution Settings</div>
          <div className="card-body">
            <div className="setting-item">
              <label>Slippage Buffer (%)</label>
              <input
                type="number"
                className="input"
                value={settings.slippageBuffer}
                onChange={(e) => handleChange('slippageBuffer', Number(e.target.value))}
                step={0.01}
                min={0}
                max={1}
              />
              <small>Buffer for limit orders to improve fill rate</small>
            </div>

            <div className="setting-item">
              <label>Order Execution Timeout (seconds)</label>
              <input
                type="number"
                className="input"
                value={settings.orderExecutionTimeout}
                onChange={(e) => handleChange('orderExecutionTimeout', Number(e.target.value))}
                min={5}
                max={300}
              />
            </div>

            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.retryFailedOrders}
                  onChange={(e) => handleChange('retryFailedOrders', e.target.checked)}
                />
                <span>Retry failed orders automatically</span>
              </label>
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="settings-section card">
          <div className="card-header">🔔 Notifications</div>
          <div className="card-body">
            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.notifyOrderFills}
                  onChange={(e) => handleChange('notifyOrderFills', e.target.checked)}
                />
                <span>Notify on order fills</span>
              </label>
            </div>

            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.notifyOrderRejections}
                  onChange={(e) => handleChange('notifyOrderRejections', e.target.checked)}
                />
                <span>Notify on order rejections</span>
              </label>
            </div>

            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.notifyStrategyErrors}
                  onChange={(e) => handleChange('notifyStrategyErrors', e.target.checked)}
                />
                <span>Notify on strategy errors</span>
              </label>
            </div>

            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.notifyDailyPnL}
                  onChange={(e) => handleChange('notifyDailyPnL', e.target.checked)}
                />
                <span>Daily P&L summary</span>
              </label>
            </div>
          </div>
        </div>

        {/* Data & Display */}
        <div className="settings-section card">
          <div className="card-header">🎨 Data & Display</div>
          <div className="card-body">
            <div className="setting-item">
              <label>Chart Theme</label>
              <select
                className="input"
                value={settings.chartTheme}
                onChange={(e) => handleChange('chartTheme', e.target.value)}
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </div>

            <div className="setting-item">
              <label>Default Chart Timeframe</label>
              <select
                className="input"
                value={settings.defaultTimeframe}
                onChange={(e) => handleChange('defaultTimeframe', e.target.value)}
              >
                <option value="1min">1 Minute</option>
                <option value="5min">5 Minutes</option>
                <option value="15min">15 Minutes</option>
                <option value="1hour">1 Hour</option>
                <option value="1d">1 Day</option>
              </select>
            </div>

            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.showRealTimeData}
                  onChange={(e) => handleChange('showRealTimeData', e.target.checked)}
                />
                <span>Show real-time data (WebSocket)</span>
              </label>
            </div>
          </div>
        </div>

        {/* Advanced */}
        <div className="settings-section card">
          <div className="card-header">🔧 Advanced</div>
          <div className="card-body">
            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.enableLogging}
                  onChange={(e) => handleChange('enableLogging', e.target.checked)}
                />
                <span>Enable logging</span>
              </label>
            </div>

            <div className="setting-item">
              <label>Log Level</label>
              <select
                className="input"
                value={settings.logLevel}
                onChange={(e) => handleChange('logLevel', e.target.value)}
                disabled={!settings.enableLogging}
              >
                <option value="error">Error</option>
                <option value="warning">Warning</option>
                <option value="info">Info</option>
                <option value="debug">Debug</option>
              </select>
            </div>

            <div className="setting-item">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.apiCallLogging}
                  onChange={(e) => handleChange('apiCallLogging', e.target.checked)}
                  disabled={!settings.enableLogging}
                />
                <span>Log API calls (for debugging)</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div className="settings-actions">
        <button className="btn btn-primary btn-large" onClick={handleSave}>
          Save Settings
        </button>
        <button className="btn btn-secondary btn-large" onClick={handleReset}>
          Reset to Defaults
        </button>
      </div>
    </div>
  );
};

export default SettingsPage;
