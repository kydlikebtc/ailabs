import { Tweet, TweetSuggestion, TweetAnalysis, ReplyOption } from '../types';

const API_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

export const twitterService = {
  async getTrendingTweets(): Promise<Tweet[]> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/twitter/trending`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get trending tweets');
    }

    return response.json();
  },

  async analyzeTweet(tweetText: string): Promise<TweetAnalysis> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/twitter/analyze`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: tweetText }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to analyze tweet');
    }

    return response.json();
  },

  async generateReplyOptions(
    tweetText: string, 
    count: number = 3, 
    isMention: boolean = false, 
    trendingScore: number = 0
  ): Promise<ReplyOption[]> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/twitter/reply-options`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        text: tweetText, 
        count,
        is_mention: isMention,
        trending_score: trendingScore
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to generate reply options');
    }

    return response.json();
  },

  async getTweetSuggestions(count: number = 3, topics?: string[]): Promise<TweetSuggestion[]> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const url = new URL(`${API_URL}/api/twitter/suggestions`);
    url.searchParams.append('count', count.toString());
    
    if (topics && topics.length > 0) {
      topics.forEach(topic => url.searchParams.append('topics', topic));
    }

    const response = await fetch(url.toString(), {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get tweet suggestions');
    }

    return response.json();
  },

  async getUserTweets(username: string, count: number = 10): Promise<Tweet[]> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const url = new URL(`${API_URL}/api/twitter/user-tweets`);
    url.searchParams.append('username', username);
    url.searchParams.append('count', count.toString());

    const response = await fetch(url.toString(), {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get user tweets');
    }

    return response.json();
  },

  async postTweet(text: string): Promise<Tweet> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/twitter/tweet`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to post tweet');
    }

    return response.json();
  },

  async replyToTweet(tweetId: string, text: string): Promise<Tweet> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/twitter/reply`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tweet_id: tweetId, text }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to reply to tweet');
    }

    return response.json();
  },

  async retweetWithComment(tweetId: string, text: string): Promise<Tweet> {
    const token = localStorage.getItem('token');
    
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${API_URL}/api/twitter/retweet`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tweet_id: tweetId, text }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to retweet with comment');
    }

    return response.json();
  }
};
