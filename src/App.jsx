import { Routes, Route } from 'react-router-dom'
import LandingLayout from './layouts/LandingLayout'
import Home from './pages/Home'

function App() {
  return (
    <Routes>
      <Route element={<LandingLayout />}>
        <Route path="/" element={<Home />} />
      </Route>
    </Routes>
  )
}

export default App
