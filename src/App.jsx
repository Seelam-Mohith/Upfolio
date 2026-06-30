import { Routes, Route } from 'react-router-dom'
import LandingLayout from './layouts/LandingLayout'
import Home from './pages/Home'
import Analyze from './pages/Analyze'
import Upload from './pages/Upload'

function App() {
  return (
    <Routes>
      <Route element={<LandingLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/analyze" element={<Analyze />} />
        <Route path="/upload" element={<Upload />} />
      </Route>
    </Routes>
  )
}

export default App
