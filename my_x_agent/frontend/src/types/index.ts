
export type PlatformType = 'twitter' | 'telegram' | 'whatsapp' | 'signal' | 'reachme';

export interface WalletInfo {
  address: string;
  connected: boolean;
}

export interface PaymentRequest {
  id: string;
  amount: number;
  itemType: string;
  status: 'pending' | 'completed' | 'failed';
  createdAt: string;
  paymentAddress: string;
}

export interface PaymentVerification {
  txId: string;
  txHash: string;
  status: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  subscription_tier: 'free' | 'pro';
  suggestions_remaining: number;
  x_username?: string;
  telegram_username?: string;
  whatsapp_phone?: string;
  signal_phone?: string;
  reachme_username?: string;
  wallet_address?: string;
  created_at: string;
  updated_at: string;
}

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials extends AuthCredentials {
  username: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Tweet {
  id: string;
  text: string;
  createdAt: string;
  likes: number;
  retweets: number;
  replies: number;
  author: {
    username: string;
    displayName: string;
    profileImageUrl: string;
  };
  isMention?: boolean;
  trendingScore?: number;
  platform?: PlatformType;
}

export interface TweetSuggestion {
  id: string;
  text: string;
  topics: string[];
  confidence: number;
  createdAt: string;
}

export interface TweetAnalysis {
  sentiment: 'positive' | 'negative' | 'neutral';
  topics: string[];
  engagement: {
    estimated: number;
    reason: string;
  };
  riskAssessment: {
    level: 'low' | 'medium' | 'high';
    reason: string;
  };
}

export interface ReplyOption {
  id: string;
  text: string;
  stance: 'supportive' | 'against' | 'neutral';
  confidence: number;
  isForMention?: boolean;
  isForTrending?: boolean;
}

export interface Subscription {
  plan: 'free' | 'pro';
  suggestionsRemaining: number;
  expiresAt?: string;
}

export interface AppState {
  user: User | null;
  isAuthenticated: boolean;
  tweetSuggestions: TweetSuggestion[];
  userTweets: Tweet[];
  isLoading: boolean;
  error: string | null;
}
