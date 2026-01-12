import React, { useState } from 'react';
import { useAuthStore } from '../../store/authStore';
import BacktestPanel from '../backtest/BacktestPanel';
import './Dashboard.css';

type Tab = 'overview' | 'strategies' | 'builder' | 'backtest' | 'settings';

const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('overview');
  const { isPaperTrading, logout } = useAuthStore();

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>🦙 AlpacaDesk</h1>
          <span className={`trading-mode ${isPaperTrading ? 'paper' : 'live'}`}>
            {isPaperTrading ? '📄 PAPER' : '🔴 LIVE'}
          </span>
        </div>
        <div className="header-right">
          <button className="btn btn-small" onClick={logout}>
            Logout
          </button>
        </div>
      </header>

      <nav className="dashboard-nav">
        <button
          className={`nav-item ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button
          className={`nav-item ${activeTab === 'strategies' ? 'active' : ''}`}
          onClick={() => setActiveTab('strategies')}
        >
          📈 Strategies
        </button>
        <button
          className={`nav-item ${activeTab === 'builder' ? 'active' : ''}`}
          onClick={() => setActiveTab('builder')}
        >
          🔧 Strategy Builder
        </button>
        <button
          className={`nav-item ${activeTab === 'backtest' ? 'active' : ''}`}
          onClick={() => setActiveTab('backtest')}
        >
          📉 Backtest
        </button>
        <button
          className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          ⚙️ Settings
        </button>
      </nav>

      <main className="dashboard-content">
        {activeTab === 'overview' && <OverviewTab />}
        {activeTab === 'strategies' && <StrategiesTab />}
        {activeTab === 'builder' && <BuilderTab />}
        {activeTab === 'backtest' && <BacktestTab />}
        {activeTab === 'settings' && <SettingsTab />}
      </main>
    </div>
  );
};

const OverviewTab: React.FC = () => {
  return (
    <div className="overview-tab">
      <h2>Portfolio Overview</h2>
      <div className="stats-grid">
        <div className="stat-card card">
          <div className="card-body">
            <div className="stat-label">Portfolio Value</div>
            <div className="stat-value">$100,000.00</div>
            <div className="stat-change positive">+$2,456.78 (+2.52%)</div>
          </div>
        </div>
        <div className="stat-card card">
          <div className="card-body">
            <div className="stat-label">Buying Power</div>
            <div className="stat-value">$95,000.00</div>
          </div>
        </div>
        <div className="stat-card card">
          <div className="card-body">
            <div className="stat-label">Active Strategies</div>
            <div className="stat-value">3</div>
          </div>
        </div>
        <div className="stat-card card">
          <div className="card-body">
            <div className="stat-label">Open Positions</div>
            <div className="stat-value">5</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StrategiesTab: React.FC = () => {
  return (
    <div className="strategies-tab">
      <h2>Pre-Built Strategies</h2>
      <p>Choose from proven algorithmic trading strategies</p>
      <div className="strategy-grid">
        <div className="strategy-card card">
          <div className="card-header">📈 Momentum Breakout</div>
          <div className="card-body">
            <p>Buy when price exceeds N-day high with volume confirmation</p>
            <button className="btn btn-primary">Deploy Strategy</button>
          </div>
        </div>
        <div className="strategy-card card">
          <div className="card-header">📉 Mean Reversion RSI</div>
          <div className="card-body">
            <p>Buy when RSI oversold + price above 200MA</p>
            <button className="btn btn-primary">Deploy Strategy</button>
          </div>
        </div>
      </div>
    </div>
  );
};

const BuilderTab: React.FC = () => {
  return (
    <div className="builder-tab">
      <h2>Visual Strategy Builder</h2>
      <p>Create custom strategies with drag-and-drop blocks</p>
      <div className="builder-placeholder">
        <p>Builder interface coming soon...</p>
      </div>
    </div>
  );
};

const BacktestTab: React.FC = () => {
  return <BacktestPanel />;
};

const SettingsTab: React.FC = () => {
  return (
    <div className="settings-tab">
      <h2>Settings</h2>
      <p>Configure your AlpacaDesk preferences</p>
    </div>
  );
};

export default Dashboard;
