import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Twitter } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { authService } from '../services/authService';
import { AuthCredentials, RegisterCredentials } from '../types';

export function Auth() {
  const { dispatch } = useAppContext();
  const [isLoading, setIsLoading] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    username: ''
  });
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      if (authMode === 'login') {
        const credentials: AuthCredentials = {
          email: formData.email,
          password: formData.password
        };

        await authService.login(credentials);
        
        const userData = await authService.getCurrentUser();
        
        dispatch({ type: 'SET_USER', payload: userData });
        dispatch({ type: 'SET_LOADING', payload: false });
        
      } else {
        if (formData.password !== formData.confirmPassword) {
          throw new Error('Passwords do not match');
        }

        const credentials: RegisterCredentials = {
          email: formData.email,
          password: formData.password,
          username: formData.username
        };

        const userData = await authService.register(credentials);
        
        await authService.login({
          email: formData.email,
          password: formData.password
        });
        
        dispatch({ type: 'SET_USER', payload: userData });
        dispatch({ type: 'SET_LOADING', payload: false });
      }
    } catch (err) {
      console.error('Authentication error:', err);
      setError(err instanceof Error ? err.message : 'Authentication failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTwitterAuth = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      alert('Twitter authentication would be initiated here');
      setTimeout(() => {
        setIsLoading(false);
      }, 1500);
    } catch (err) {
      console.error('Twitter auth error:', err);
      setError(err instanceof Error ? err.message : 'Twitter authentication failed');
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">My X Agent</CardTitle>
          <CardDescription className="text-center">
            {authMode === 'login' ? 'Sign in to your account' : 'Create a new account'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <Button 
              variant="outline" 
              className="w-full" 
              onClick={handleTwitterAuth}
              disabled={isLoading}
            >
              <Twitter className="mr-2 h-4 w-4" />
              {authMode === 'login' ? 'Sign in with X' : 'Sign up with X'}
            </Button>
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white dark:bg-gray-950 px-2 text-muted-foreground">
                  Or continue with
                </span>
              </div>
            </div>
            {error && (
              <div className="p-3 text-sm text-white bg-red-500 rounded">
                {error}
              </div>
            )}
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input 
                    id="email" 
                    type="email" 
                    placeholder="m@example.com" 
                    required 
                    value={formData.email}
                    onChange={handleInputChange}
                  />
                </div>
                {authMode === 'register' && (
                  <div className="space-y-2">
                    <Label htmlFor="username">Username</Label>
                    <Input 
                      id="username" 
                      type="text" 
                      required 
                      value={formData.username}
                      onChange={handleInputChange}
                    />
                  </div>
                )}
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input 
                    id="password" 
                    type="password" 
                    required 
                    value={formData.password}
                    onChange={handleInputChange}
                  />
                </div>
                {authMode === 'register' && (
                  <div className="space-y-2">
                    <Label htmlFor="confirmPassword">Confirm Password</Label>
                    <Input 
                      id="confirmPassword" 
                      type="password" 
                      required 
                      value={formData.confirmPassword}
                      onChange={handleInputChange}
                    />
                  </div>
                )}
                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? 'Processing...' : authMode === 'login' ? 'Sign In' : 'Sign Up'}
                </Button>
              </div>
            </form>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col">
          <div className="text-center text-sm">
            {authMode === 'login' ? (
              <span>
                Don't have an account?{' '}
                <button
                  className="underline underline-offset-4 hover:text-primary"
                  onClick={() => setAuthMode('register')}
                  type="button"
                >
                  Sign up
                </button>
              </span>
            ) : (
              <span>
                Already have an account?{' '}
                <button
                  className="underline underline-offset-4 hover:text-primary"
                  onClick={() => setAuthMode('login')}
                  type="button"
                >
                  Sign in
                </button>
              </span>
            )}
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
