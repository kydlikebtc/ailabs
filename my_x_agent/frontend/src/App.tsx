import { useState } from 'react'
import './App.css'
import { MainNav } from './components/MainNav'
import { Dashboard } from './components/Dashboard'
import { TweetSuggestions } from './components/TweetSuggestions'
import { Auth } from './components/Auth'
import { AppProvider, useAppContext } from './context/AppContext'

function MainApp() {
  const { state } = useAppContext();
  const [currentPage, setCurrentPage] = useState<'dashboard' | 'suggestions'>('dashboard');

  const handleNavigation = (page: 'dashboard' | 'suggestions') => {
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
