import React, { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { AppState, User, TweetSuggestion, Tweet } from '../types';
import { authService } from '../services/authService';

const initialState: AppState = {
  user: null,
  isAuthenticated: false,
  tweetSuggestions: [],
  userTweets: [],
  isLoading: false,
  error: null
};

type Action =
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'SET_AUTHENTICATED'; payload: boolean }
  | { type: 'SET_TWEET_SUGGESTIONS'; payload: TweetSuggestion[] }
  | { type: 'ADD_TWEET_SUGGESTION'; payload: TweetSuggestion }
  | { type: 'REMOVE_TWEET_SUGGESTION'; payload: string }
  | { type: 'SET_USER_TWEETS'; payload: Tweet[] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'LOGOUT' };

function appReducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'SET_USER':
      return { 
        ...state, 
        user: action.payload,
        isAuthenticated: !!action.payload
      };
    case 'SET_AUTHENTICATED':
      return { ...state, isAuthenticated: action.payload };
    case 'SET_TWEET_SUGGESTIONS':
      return { ...state, tweetSuggestions: action.payload };
    case 'ADD_TWEET_SUGGESTION':
      return { 
        ...state, 
        tweetSuggestions: [action.payload, ...state.tweetSuggestions] 
      };
    case 'REMOVE_TWEET_SUGGESTION':
      return { 
        ...state, 
        tweetSuggestions: state.tweetSuggestions.filter(
          suggestion => suggestion.id !== action.payload
        ) 
      };
    case 'SET_USER_TWEETS':
      return { ...state, userTweets: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'LOGOUT':
      return {
        ...initialState
      };
    default:
      return state;
  }
}

type AppContextType = {
  state: AppState;
  dispatch: React.Dispatch<Action>;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

interface AppProviderProps {
  children: ReactNode;
}

export function AppProvider({ children }: AppProviderProps) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  useEffect(() => {
    const initializeAuth = async () => {
      if (authService.isAuthenticated()) {
        dispatch({ type: 'SET_LOADING', payload: true });
        try {
          const userData = await authService.getCurrentUser();
          dispatch({ type: 'SET_USER', payload: userData });
        } catch (error) {
          console.error('Failed to restore authentication:', error);
          authService.logout();
        } finally {
          dispatch({ type: 'SET_LOADING', payload: false });
        }
      }
    };

    initializeAuth();
  }, []);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}
