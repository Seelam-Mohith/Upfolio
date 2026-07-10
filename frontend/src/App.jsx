import { Routes, Route } from 'react-router-dom'
import LandingLayout from './layouts/LandingLayout'
import Home from './pages/Home'
import Upload from './pages/Upload'

function App() {
  return (
    <Routes>
      <Route element={<LandingLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/analyze" element={<Upload />} />
      </Route>
    </Routes>
  )
}

export default App
