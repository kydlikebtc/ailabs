
export interface User {
  id: string;
  username: string;
  email: string;
  subscription_tier: 'free' | 'pro';
  suggestions_remaining: number;
  x_username?: string;
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
