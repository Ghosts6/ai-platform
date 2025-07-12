import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import React from 'react';
import Home from './pages/Home';
import Agent from './pages/Agent';
import NotFound from './pages/NotFound';
import Error500 from './pages/Error500';
import Readme from './pages/Readme';
import Contact from './pages/Contact';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/agent" element={<Agent />} />
        <Route path="/readme" element={<Readme />} />
        <Route path="/500" element={<Error500 />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
