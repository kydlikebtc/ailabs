import React, { useState } from 'react'
import './App.css'
import { MainNav } from './components/MainNav'
import { Dashboard } from './components/Dashboard'
import { TweetSuggestions } from './components/TweetSuggestions'
import { TweetAnalysis } from './components/TweetAnalysis'
import { TrendingTweets } from './components/TrendingTweets'
import { Auth } from './components/Auth'
import { AppProvider, useAppContext } from './context/AppContext'

function MainApp() {
  const { state } = useAppContext();
  const [currentPage, setCurrentPage] = useState<'dashboard' | 'suggestions' | 'analysis' | 'trending' | 'account' | 'settings'>('dashboard');

  const handleNavigation = (page: 'dashboard' | 'suggestions' | 'analysis' | 'trending' | 'account' | 'settings') => {
    setCurrentPage(page);
  };

  if (!state.isAuthenticated) {
    return <Auth />;
  }

  return (
    <div className="flex h-screen">
      <div className="w-64 hidden md:block">
        <MainNav 
          currentPage={currentPage} 
          onNavigate={handleNavigation} 
        />
      </div>
      <div className="flex-1 overflow-auto p-6">
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'suggestions' && <TweetSuggestions />}
        {currentPage === 'analysis' && <TweetAnalysis />}
        {currentPage === 'trending' && <TrendingTweets />}
        {currentPage === 'account' && <div className="p-4">Account settings coming soon</div>}
        {currentPage === 'settings' && <div className="p-4">Application settings coming soon</div>}
      </div>
    </div>
  );
}

function App() {
  return (
    <AppProvider>
      <MainApp />
    </AppProvider>
  );
}

export default App
