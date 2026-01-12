export interface Account {
  accountNumber: string;
  portfolioValue: number;
  buyingPower: number;
  cash: number;
  equity: number;
  status: string;
  patternDayTrader: boolean;
}

export interface Position {
  symbol: string;
  qty: number;
  avgEntryPrice: number;
  currentPrice: number;
  marketValue: number;
  costBasis: number;
  unrealizedPl: number;
  unrealizedPlpc: number;
  side: 'long' | 'short';
}

export interface Order {
  id: string;
  symbol: string;
  qty: number;
  filledQty: number;
  side: 'buy' | 'sell';
  type: 'market' | 'limit' | 'stop' | 'stop_limit';
  status: string;
  createdAt: string | null;
  filledAvgPrice: number | null;
}

export interface Strategy {
  id: string;
  name: string;
  type: string;
  symbols: string[];
  parameters: Record<string, any>;
  enabled: boolean;
  createdAt: string;
}

export interface StrategyTemplate {
  id: string;
  name: string;
  description: string;
  defaultParameters: Record<string, any>;
  typicalTradesPerMonth: string;
}

export interface BacktestRequest {
  strategyType: string;
  symbols: string[];
  parameters: Record<string, any>;
  startDate: string;
  endDate: string;
  initialCapital?: number;
}

export interface BacktestResult {
  totalReturn: number;
  buyAndHoldReturn: number;
  maxDrawdown: number;
  winRate: number;
  totalTrades: number;
  winningTrades: number;
  losingTrades: number;
  avgWin: number;
  avgLoss: number;
  avgTradeDurationDays: number;
  sharpeRatio: number;
  maxConsecutiveWins: number;
  maxConsecutiveLosses: number;
  equityCurve: EquityPoint[];
}

export interface EquityPoint {
  date: string;
  equity: number;
  profitLoss: number;
  profitLossPct: number;
}

export interface PortfolioHistory {
  timestamp: number[];
  equity: number[];
  profitLoss: number[];
  profitLossPct: number[];
  baseValue: number;
  timeframe: string;
}
