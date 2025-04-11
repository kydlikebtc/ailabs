import React from 'react';
import { Button } from './ui/button';
import { Home, MessageSquare, BarChart2, User, Settings, LogOut } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { authService } from '../services/authService';

interface NavItemProps {
  onClick: () => void;
  icon: React.ReactNode;
  children: React.ReactNode;
  active?: boolean;
}

function NavItem({ onClick, icon, children, active }: NavItemProps) {
  return (
    <button
      onClick={onClick}
      className={`flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm text-left transition-all hover:bg-gray-100 dark:hover:bg-gray-800 ${
        active ? 'bg-gray-100 dark:bg-gray-800' : ''
      }`}
    >
      {icon}
      <span>{children}</span>
    </button>
  );
}

interface MainNavProps {
  currentPage: 'dashboard' | 'suggestions';
  onNavigate: (page: 'dashboard' | 'suggestions') => void;
}

export function MainNav({ currentPage, onNavigate }: MainNavProps) {
  const { dispatch } = useAppContext();

  const handleLogout = () => {
    authService.logout();
    dispatch({ type: 'LOGOUT' });
  };

  return (
    <div className="flex h-screen flex-col border-r bg-white dark:bg-gray-950">
      <div className="p-6">
        <h2 className="text-xl font-bold">My X Agent</h2>
      </div>
      <div className="flex-1 overflow-auto py-2">
        <nav className="grid gap-1 px-2">
          <NavItem 
            onClick={() => onNavigate('dashboard')} 
            icon={<Home className="h-4 w-4" />} 
            active={currentPage === 'dashboard'}
          >
            Dashboard
          </NavItem>
          <NavItem 
            onClick={() => onNavigate('suggestions')} 
            icon={<MessageSquare className="h-4 w-4" />} 
            active={currentPage === 'suggestions'}
          >
            Tweet Suggestions
          </NavItem>
          <NavItem 
            onClick={() => {}} 
            icon={<BarChart2 className="h-4 w-4" />} 
            active={false}
          >
            Tweet Analysis
          </NavItem>
          <NavItem 
            onClick={() => {}} 
            icon={<User className="h-4 w-4" />} 
            active={false}
          >
            Account
          </NavItem>
          <NavItem 
            onClick={() => {}} 
            icon={<Settings className="h-4 w-4" />} 
            active={false}
          >
            Settings
          </NavItem>
        </nav>
      </div>
      <div className="mt-auto p-4">
        <Button 
          variant="ghost" 
          className="w-full justify-start"
          onClick={handleLogout}
        >
          <LogOut className="mr-2 h-4 w-4" />
          Logout
        </Button>
      </div>
    </div>
  );
}
