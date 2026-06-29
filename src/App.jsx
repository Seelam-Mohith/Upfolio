import { Routes, Route } from 'react-router-dom'
import LandingLayout from './layouts/LandingLayout'
import Home from './pages/Home'
import Analyze from './pages/Analyze'

function App() {
  return (
    <Routes>
      <Route element={<LandingLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/analyze" element={<Analyze />} />
      </Route>
    </Routes>
  )
}

export default App
