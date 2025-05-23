import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { HashRouter as Router } from 'react-router-dom'; // To provide context for useNavigate
import LoginPage from './LoginPage';
import { AuthProvider, useAuth } from '../../context/AuthContext'; // To mock useAuth

// Mock react-router-dom's useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock the useAuth hook
const mockLogin = jest.fn();
// const mockUseAuth = useAuth as jest.Mock; // Cast for type safety if needed, or define specific mock type

jest.mock('../../context/AuthContext', () => ({
  ...jest.requireActual('../../context/AuthContext'),
  useAuth: jest.fn(() => ({
    login: mockLogin,
    isAuthenticated: false,
    isLoading: false,
    // Add other properties from AuthContextType if needed by the component during render
    accessToken: null,
    refreshToken: null,
    user: null,
    logout: jest.fn(), 
  })),
}));


// Mock global fetch
global.fetch = jest.fn();

describe('LoginPage', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockLogin.mockClear();
    mockNavigate.mockClear();
    (global.fetch as jest.Mock).mockClear();
    localStorage.clear(); // Clear localStorage
  });

  const renderComponent = () => {
    // AuthProvider might not be strictly necessary here if useAuth is fully mocked,
    // but wrapping with Router is good practice for components using router features.
    // If LoginPage directly used context for other things, AuthProvider would be needed.
    return render(
      <Router> 
        <AuthProvider> {/* Or provide a simplified mock context provider if preferred */}
          <LoginPage />
        </AuthProvider>
      </Router>
    );
  };

  test('renders login form correctly', () => {
    renderComponent();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  test('allows typing in email and password fields', () => {
    renderComponent();
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    expect(screen.getByLabelText(/email/i)).toHaveValue('test@example.com');
    expect(screen.getByLabelText(/password/i)).toHaveValue('password123');
  });

  test('calls login function and navigates on successful submission', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ access: 'fakeAccessToken', refresh: 'fakeRefreshToken', user_id: '123' }),
    });

    renderComponent();

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('fakeAccessToken', 'fakeRefreshToken', { id: '123', email: 'test@example.com' });
    });
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/');
    });
  });

  test('shows error message on failed submission', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Invalid credentials' }),
    });

    renderComponent();

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
    expect(mockLogin).not.toHaveBeenCalled();
    expect(mockNavigate).not.toHaveBeenCalled();
  });
  
  test('shows generic error message on network error', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    renderComponent();
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/an unexpected error occurred/i)).toBeInTheDocument();
    });
  });
});
