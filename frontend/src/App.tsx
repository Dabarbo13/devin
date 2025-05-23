import { Routes, Route, Link } from 'react-router-dom'; // Removed useNavigate, Router is in main.tsx
import './App.css';

import ClinicalTrials from './components/ClinicalTrials';
import DonationManagement from './components/DonationManagement';
import Recruiting from './components/Recruiting';
import SponsorPortal from './components/SponsorPortal';
import WebStore from './components/WebStore';
import LoginPage from './pages/LoginPage';
import { useAuth } from './context/AuthContext';
import { Button } from './components/ui/button';
import ProtectedRoute from './components/ProtectedRoute'; // Added
import Dashboard from './components/Dashboard'; // Added

function App() {
  // useNavigate is removed from here as Router is now in main.tsx, 
  // but App still needs useAuth for logout and conditional UI
  const { isAuthenticated, logout, isLoading } = useAuth(); 
  // const navigate = useNavigate(); // No longer using navigate directly in App.tsx for logout redirection logic.
                                 // Logout in AuthContext might handle this, or ProtectedRoute handles redirection.
                                 // For the button, it's simpler to just call logout and let effects handle redirection.

  const handleLogout = () => {
    logout();
    // Navigation to '/login' will be handled by ProtectedRoute or if AuthContext's logout forces a state
    // change that makes isAuthenticated false, which in turn makes ProtectedRoute redirect.
    // Or, if preferred, can explicitly navigate here if Router context is available (e.g. if App is wrapped in Router)
    // For now, relying on AuthContext + ProtectedRoute behavior.
    // If direct navigation is needed after logout from App.tsx, ensure Router wraps App or use alternative.
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  return (
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-md p-4">
          <div className="container mx-auto flex justify-between items-center">
            <Link to="/" className="text-xl font-bold">Biobank Platform</Link>
            <div className="space-x-4 flex items-center">
              {isAuthenticated ? (
                <>
                  <Link to="/" className="text-blue-600 hover:text-blue-800">Dashboard</Link>
                  <Link to="/clinical-trials" className="text-blue-600 hover:text-blue-800">Clinical Trials</Link>
                  {/* Add other authenticated links here */}
                  <Button variant="outline" onClick={handleLogout}>Logout</Button>
                </>
              ) : (
                <>
                  {/* Links visible when not authenticated */}
                  <Link to="/login" className="text-blue-600 hover:text-blue-800">Login</Link>
                  {/* Potentially a public registration link here */}
                </>
              )}
            </div>
          </div>
        </nav>
        
        <main className="container mx-auto mt-8">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/clinical-trials/*" 
              element={
                <ProtectedRoute>
                  <ClinicalTrials />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/donation-management/*" 
              element={
                <ProtectedRoute>
                  <DonationManagement />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/recruiting/*" 
              element={
                <ProtectedRoute>
                  <Recruiting />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/sponsor-portal/*" 
              element={
                <ProtectedRoute>
                  <SponsorPortal />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/store/*" 
              element={
                <ProtectedRoute>
                  <WebStore />
                </ProtectedRoute>
              } 
            />
            {/* Consider adding a NotFoundPage component for a catch-all route */}
            {/* <Route path="*" element={<NotFoundPage />} /> */}
          </Routes>
        </main>
      </div>
  );
}

export default App;
