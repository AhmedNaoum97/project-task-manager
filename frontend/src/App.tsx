import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';



function App() {
  const { token } = useAuth();

  return (
      <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/" element={token ? <Navigate to="/tasks" /> : <Navigate to="/login" />} />
        <Route path="/tasks" element={token ? <div>Tasks Page (Coming Soon)</div> : <Navigate to="/login" />} />
      </Routes>
      </BrowserRouter>
    );
  }

export default App;