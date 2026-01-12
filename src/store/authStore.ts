import { create } from 'zustand';

interface AuthState {
  isAuthenticated: boolean;
  isPaperTrading: boolean;
  apiKeyId: string | null;
  setAuthenticated: (value: boolean) => void;
  setPaperTrading: (value: boolean) => void;
  setApiKeyId: (value: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  isPaperTrading: false,
  apiKeyId: null,
  setAuthenticated: (value) => set({ isAuthenticated: value }),
  setPaperTrading: (value) => set({ isPaperTrading: value }),
  setApiKeyId: (value) => set({ apiKeyId: value }),
  logout: () => set({ isAuthenticated: false, apiKeyId: null }),
}));
