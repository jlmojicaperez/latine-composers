import './App.css'
import { Route, Routes } from 'react-router-dom'
import ComposersPage from './pages/ComposersPages/ComposersPage'
import ComposerPage from './pages/ComposersPages/ComposerPage'
import ComposerList from './pages/ComposersPages/components/ComposerList'


function App() {
  return <Routes>
    <Route path="/" element={<ComposersPage />} />
    <Route path="/composers/:composer_id" element={<ComposerPage />} />
    <Route path="/culo" element={<ComposerList />} />
  </Routes>
}

export default App
