import { PaymentRequest, PaymentVerification } from '../types';

const API_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

export const paymentService = {
  async createPaymentRequest(itemType: string, quantity: number = 1): Promise<PaymentRequest> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/payment/request`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ item_type: itemType, quantity }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create payment request');
    }

    return response.json();
  },

  async verifyPayment(txId: string, txHash: string): Promise<PaymentVerification> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/payment/verify`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tx_id: txId, tx_hash: txHash }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to verify payment');
    }

    return response.json();
  },

  async getPaymentStatus(txId: string): Promise<PaymentRequest> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/payment/status/${txId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get payment status');
    }

    return response.json();
  },

  async getPaymentHistory(): Promise<PaymentRequest[]> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/payment/history`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get payment history');
    }

    return response.json();
  },

  calculateBNBPrice(itemType: string, quantity: number = 1): number {
    if (itemType === 'tweet_suggestion') {
      return 0.015 * quantity; // 每条推文建议0.015 BNB
    }
    return 0;
  },

  async connectWallet(): Promise<string> {
    if (typeof window.ethereum !== 'undefined') {
      try {
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        return accounts[0];
      } catch (error) {
        throw new Error('Failed to connect wallet: ' + error.message);
      }
    } else {
      throw new Error('No Web3 provider detected. Please install MetaMask or another wallet.');
    }
  }
};

declare global {
  interface Window {
    ethereum?: {
      request: (args: { method: string; params?: any[] }) => Promise<any>;
      on: (event: string, callback: (...args: any[]) => void) => void;
      removeListener: (event: string, callback: (...args: any[]) => void) => void;
      selectedAddress: string | null;
    };
  }
}
