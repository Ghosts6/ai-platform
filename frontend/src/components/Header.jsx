import React, { useState, useEffect } from 'react';
import { FaUserCircle } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

export default function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const navigate = useNavigate();

  useEffect(() => {
    const handleStorage = () => setIsLoggedIn(!!localStorage.getItem('token'));
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    navigate('/');
  };

  return (
    <header className="w-full bg-secondary text-accent py-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-4">
        <a href="/" className="flex items-center group">
          <span className="logo-icon-wrapper mr-1">
            <img src="/img/logo.png" alt="AIAgent Logo" className="h-8 w-8 transition-transform duration-300 ease-in-out logo-hover" />
          </span>
          <h1 className="text-2xl font-bold tracking-wide text-primary logo-text-animate">AIAgent</h1>
        </a>
        <nav className="space-x-4 flex items-center">
          <a href="/" className="nav-link">Home</a>
          <a href="/agent" className="nav-link">Agent</a>
          <a href="/readme" className="nav-link">README</a>
          <a href="/contact" className="nav-link">Contact</a>
          {isLoggedIn ? (
            <button onClick={handleLogout} className="logout-button-nav">Logout</button>
          ) : (
            <a href="/login" className="login-button-header">Login</a>
          )}
        </nav>
      </div>
    </header>
  );
}