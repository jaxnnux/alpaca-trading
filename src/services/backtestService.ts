import axios from 'axios';
import { BacktestRequest, BacktestResult } from '../types';

const API_BASE_URL = 'http://localhost:8765';

class BacktestService {
  async runBacktest(request: BacktestRequest): Promise<BacktestResult> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/backtest/run`, request);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to run backtest');
    }
  }

  async getTemplates(): Promise<any> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/backtest/templates`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to get templates');
    }
  }
}

export const backtestService = new BacktestService();
