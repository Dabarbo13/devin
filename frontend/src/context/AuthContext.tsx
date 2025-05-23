import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define the shape of the user object (can be expanded later)
interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  // Add other relevant user fields, e.g., roles
}

// Define the shape of the auth state
interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

// Define the shape of the context value
interface AuthContextType extends AuthState {
  login: (access: string, refresh: string, userData: User) => void;
  logout: () => void;
  // We can add a function for token refresh here later if needed by components directly
  // e.g., refreshAuthToken: () => Promise<string | null>; 
}

// Create the context with a default undefined value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define the props for the AuthProvider
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>({
    accessToken: null,
    refreshToken: null,
    user: null,
    isAuthenticated: false,
    isLoading: true, // Start with loading true to check initial token status
  });

  useEffect(() => {
    // Attempt to load tokens from storage on initial load
    const access = localStorage.getItem('accessToken');
    const refresh = localStorage.getItem('refreshToken');
    const storedUser = localStorage.getItem('user'); // User info might also be stored

    if (access && refresh) {
      // Here, you might want to verify the token with the backend or decode it
      // For now, we'll assume if tokens exist, the user is "authenticated"
      // User data also needs to be parsed if stored
      let parsedUser: User | null = null;
      if (storedUser) {
        try {
          parsedUser = JSON.parse(storedUser);
        } catch (e) {
          console.error("Failed to parse stored user:", e);
        }
      }
      
      setAuthState({
        accessToken: access,
        refreshToken: refresh,
        user: parsedUser, // Set user if available
        isAuthenticated: true,
        isLoading: false,
      });
    } else {
      setAuthState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  const login = (access: string, refresh: string, userData: User) => {
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    localStorage.setItem('user', JSON.stringify(userData)); // Store user data
    setAuthState({
      accessToken: access,
      refreshToken: refresh,
      user: userData,
      isAuthenticated: true,
      isLoading: false,
    });
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user'); // Remove user data
    setAuthState({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
    });
    // Optionally, redirect to login page or notify backend
  };

  return (
    <AuthContext.Provider value={{ ...authState, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
