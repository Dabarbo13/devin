import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

import ClinicalTrials from './components/ClinicalTrials'
import DonationManagement from './components/DonationManagement'
import Recruiting from './components/Recruiting'
import SponsorPortal from './components/SponsorPortal'
import WebStore from './components/WebStore'

const Dashboard = () => (
  <div className="p-4">
    <h1 className="text-2xl font-bold mb-6">Biobank Platform Dashboard</h1>
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-2">Clinical Trials</h2>
        <p className="text-gray-600 mb-2">3 active studies</p>
        <p className="text-gray-600">25 enrolled participants</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-2">Donations</h2>
        <p className="text-gray-600 mb-2">15 donations this month</p>
        <p className="text-gray-600">120 samples in inventory</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-2">Recruiting</h2>
        <p className="text-gray-600 mb-2">45 active prospects</p>
        <p className="text-gray-600">12 qualified leads</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-2">Sponsor Portal</h2>
        <p className="text-gray-600 mb-2">8 active sponsors</p>
        <p className="text-gray-600">5 pending sample requests</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-2">Web Store</h2>
        <p className="text-gray-600 mb-2">25 products available</p>
        <p className="text-gray-600">10 orders this month</p>
      </div>
      <div className="bg-white p-4 rounded-lg shadow">
        <h2 className="text-lg font-semibold mb-2">System Status</h2>
        <p className="text-gray-600 mb-2">All systems operational</p>
        <p className="text-gray-600">Last backup: Today at 12:00</p>
      </div>
    </div>
  </div>
)

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-md p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold">Biobank Platform</h1>
            <div className="space-x-4">
              <a href="/" className="text-blue-600 hover:text-blue-800">Dashboard</a>
              <a href="/clinical-trials" className="text-blue-600 hover:text-blue-800">Clinical Trials</a>
              <a href="/donation-management" className="text-blue-600 hover:text-blue-800">Donations</a>
              <a href="/recruiting" className="text-blue-600 hover:text-blue-800">Recruiting</a>
              <a href="/sponsor-portal" className="text-blue-600 hover:text-blue-800">Sponsor Portal</a>
              <a href="/store" className="text-blue-600 hover:text-blue-800">Store</a>
            </div>
          </div>
        </nav>
        
        <main className="container mx-auto mt-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/clinical-trials/*" element={<ClinicalTrials />} />
            <Route path="/donation-management/*" element={<DonationManagement />} />
            <Route path="/recruiting/*" element={<Recruiting />} />
            <Route path="/sponsor-portal/*" element={<SponsorPortal />} />
            <Route path="/store/*" element={<WebStore />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
