import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

const Dashboard = () => <div className="p-4"><h1 className="text-2xl font-bold">Dashboard</h1></div>
const ClinicalTrials = () => <div className="p-4"><h1 className="text-2xl font-bold">Clinical Trial Management</h1></div>
const DonationManagement = () => <div className="p-4"><h1 className="text-2xl font-bold">Donation Management</h1></div>
const Recruiting = () => <div className="p-4"><h1 className="text-2xl font-bold">Recruiting Platform</h1></div>
const SponsorPortal = () => <div className="p-4"><h1 className="text-2xl font-bold">Sponsor Portal</h1></div>
const WebStore = () => <div className="p-4"><h1 className="text-2xl font-bold">Web Store</h1></div>

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
