import './App.css'
import { Route, Routes } from 'react-router-dom'
import ComposerProfilePage from './pages/ComposersPages/ComposerProfilePage'
import ComposersListPage from './pages/ComposersPages/ComposersListPage'
import ComposerEditPage from './pages/ComposersPages/ComposerEditPage'


function App() {
  return <Routes>
    <Route path="/" element={<ComposersListPage />} />
    <Route path="/composers/:composer_id" element={<ComposerProfilePage />} />
    <Route path="/composers/:composer_id/edit" element={<ComposerEditPage />} />
  </Routes>
}

export default App
