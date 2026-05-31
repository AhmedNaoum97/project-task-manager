import { createContext, useState, useContext, ReactNode } from 'react';
import { authService } from '../services/api';

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem('token')
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const signup = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.signup(email, password);
      const { user: newUser, token: newToken } = response.data.data;
      setUser(newUser);
      setToken(newToken);
      localStorage.setItem('token', newToken);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Signup failed');
    } finally {
      setIsLoading(false);
    }
  };

const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.login(email, password);
      const { user: newUser, token: newToken } = response.data.data;
      setUser(newUser);
      setToken(newToken);
      localStorage.setItem('token', newToken);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
};

return (
    <AuthContext.Provider value={{user, token, login, signup, logout, isLoading, error }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}