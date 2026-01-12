import React, { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { authService } from '../services/authService';
import './LoginPage.css';

const LoginPage: React.FC = () => {
  const [apiKeyId, setApiKeyId] = useState('');
  const [secretKey, setSecretKey] = useState('');
  const [isPaper, setIsPaper] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { setAuthenticated, setPaperTrading, setApiKeyId: setStoredApiKeyId } = useAuthStore();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Validate API keys with Alpaca
      const result = await authService.login(apiKeyId, secretKey, isPaper);

      if (result.success) {
        setStoredApiKeyId(apiKeyId);
        setPaperTrading(isPaper);
        setAuthenticated(true);
      } else {
        setError(result.error || 'Failed to authenticate with Alpaca');
      }
    } catch (err) {
      setError('Connection error. Please check your credentials and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>🦙 AlpacaDesk</h1>
          <p>Native Windows Algorithmic Trading Application</p>
        </div>

        <div className="login-card card">
          <div className="card-header">
            <h2>Connect Alpaca Account</h2>
          </div>
          <div className="card-body">
            <div className="security-notice">
              <div className="security-icon">🔐</div>
              <div>
                <h3>YOUR API KEYS STAY ON THIS COMPUTER</h3>
                <p>Unlike cloud platforms, AlpacaDesk stores your credentials locally using Windows encryption. We never see or transmit your keys.</p>
              </div>
            </div>

            <form onSubmit={handleLogin}>
              <div className="form-group">
                <label htmlFor="apiKeyId">API Key ID:</label>
                <input
                  id="apiKeyId"
                  type="text"
                  className="input"
                  value={apiKeyId}
                  onChange={(e) => setApiKeyId(e.target.value)}
                  placeholder="PK..."
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="secretKey">Secret Key:</label>
                <input
                  id="secretKey"
                  type="password"
                  className="input"
                  value={secretKey}
                  onChange={(e) => setSecretKey(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="checkbox-label">
                  <input
                    type="radio"
                    checked={isPaper}
                    onChange={() => setIsPaper(true)}
                  />
                  <span>I'm using a PAPER trading account (recommended)</span>
                </label>
                <label className="checkbox-label">
                  <input
                    type="radio"
                    checked={!isPaper}
                    onChange={() => setIsPaper(false)}
                  />
                  <span>I'm using a LIVE trading account</span>
                </label>
              </div>

              {error && <div className="error-message">{error}</div>}

              <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
                {loading ? 'Connecting...' : 'Connect & Continue →'}
              </button>

              <div className="help-link">
                <a href="https://alpaca.markets/docs/api-references/" target="_blank" rel="noopener noreferrer">
                  📚 Get API Keys from Alpaca ↗
                </a>
              </div>
            </form>
          </div>
        </div>

        <div className="onboarding-progress">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: '33%' }}></div>
          </div>
          <div className="progress-text">Step 1 of 3: Connect Alpaca Account</div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
