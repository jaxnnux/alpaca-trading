import axios from 'axios';

const API_BASE_URL = 'http://localhost:8765';

interface LoginResult {
  success: boolean;
  error?: string;
}

class AuthService {
  async login(apiKeyId: string, secretKey: string, isPaper: boolean): Promise<LoginResult> {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
        api_key_id: apiKeyId,
        secret_key: secretKey,
        is_paper: isPaper,
      });

      if (response.data.success) {
        return { success: true };
      } else {
        return { success: false, error: response.data.message };
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Failed to connect to backend',
      };
    }
  }

  async logout(): Promise<void> {
    try {
      await axios.post(`${API_BASE_URL}/api/auth/logout`);
    } catch (error) {
      console.error('Logout error:', error);
    }
  }

  async validateCredentials(): Promise<boolean> {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/auth/validate`);
      return response.data.valid;
    } catch (error) {
      return false;
    }
  }
}

export const authService = new AuthService();
