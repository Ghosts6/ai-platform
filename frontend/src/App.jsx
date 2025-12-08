import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import React from 'react';
import Home from './pages/Home';
import ChatbotHome from './pages/ChatbotHome';
import ChatbotChat from './pages/ChatbotChat';
import Agents from './pages/Agents';
import Agent from './pages/Agent';
import Login from './pages/Login';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import NotFound from './pages/NotFound';
import Error500 from './pages/Error500';
import Readme from './pages/Readme';
import Contact from './pages/Contact';
import ScrollToTop from './components/ScrollToTop';


import ChatHistory from './pages/ChatHistory';
import ChatSession from './pages/ChatSession';
import AgentHistory from './pages/AgentHistory';

function App() {
  return (
    <Router>
      <ScrollToTop />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chatbot" element={<ChatbotHome />} />
        <Route path="/chatbot/new" element={<ChatbotChat />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/agent" element={<Agent />} />
        <Route path="/agent/history" element={<AgentHistory />} />
        <Route path="/chatbot/history" element={<ChatHistory />} />
        <Route path="/chatbot/session/:sessionId" element={<ChatSession />} />
        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/readme" element={<Readme />} />
        <Route path="/500" element={<Error500 />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;