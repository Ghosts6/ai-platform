import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Agent from './pages/Agent';
import NotFound from './pages/NotFound';
import Error500 from './pages/Error500';
import './App.css';

function App() {
  return (
    <Router>
      <nav className="bg-white dark:bg-gray-800 shadow p-4 flex gap-4">
        <Link to="/" className="text-blue-600 font-semibold hover:underline">Home</Link>
        <Link to="/agent" className="text-green-600 font-semibold hover:underline">Agent</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/agent" element={<Agent />} />
        <Route path="/500" element={<Error500 />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
