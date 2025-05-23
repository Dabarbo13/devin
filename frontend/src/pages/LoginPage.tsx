import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Added
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { useAuth } from '../../context/AuthContext'; // Added

// Define a basic structure for what the token endpoint might return for user data
// This is a placeholder and should be adjusted based on actual API response or JWT content.
interface BasicUser {
  id: string;
  email: string;
  // Potentially other fields like first_name, last_name if the token or a related endpoint provides them
}

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const navigate = useNavigate(); // Added
  const { login } = useAuth(); // Added

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/token/', { // Ensure this matches your backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Assuming data contains access and refresh tokens
        // And potentially some basic user info, or we decode it from token, or fetch separately.
        // For now, creating a placeholder user object.
        // A more robust solution would involve fetching user details or decoding the JWT.
        const userData: BasicUser = { 
            id: data.user_id || 'temp-user-id', // Adjust if your token endpoint returns user_id
            email: email 
        }; 
        
        login(data.access, data.refresh, userData);
        navigate('/'); // Navigate to dashboard or home page
      } else {
        // Handle errors (e.g., invalid credentials, server error)
        setError(data.detail || data.message || 'Login failed. Please check your credentials.');
      }
    } catch (err) {
      console.error('Login request error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">Login</CardTitle>
          <CardDescription className="text-center">
            Enter your credentials to access the Biobank Platform.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isLoading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isLoading}
              />
            </div>
            {error && <p className="text-sm text-red-600">{error}</p>}
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Logging in...' : 'Login'}
            </Button>
          </form>
        </CardContent>
        {/* Footer remains the same */}
      </Card>
    </div>
  );
};

export default LoginPage;
