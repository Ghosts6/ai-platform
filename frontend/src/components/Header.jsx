import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBars, FaTimes } from 'react-icons/fa';

export default function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleStorage = () => setIsLoggedIn(!!localStorage.getItem('token'));
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setIsMenuOpen(false);
    navigate('/');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="w-full bg-secondary text-accent py-4 shadow-lg relative z-50">
      <div className="container mx-auto flex justify-between items-center px-4">
        <a href="/" className="flex items-center group">
          <span className="logo-icon-wrapper mr-1">
            <img src="/img/logo.png" alt="AIAgent Logo" className="h-8 w-8 transition-transform duration-300 ease-in-out logo-hover" />
          </span>
          <h1 className="text-2xl font-bold tracking-wide text-primary logo-text-animate">AIAgent</h1>
        </a>
        <nav className="hidden md:flex space-x-4 items-center">
          <a href="/" className="nav-link">Home</a>
          <a href="/agent" className="nav-link">Agent</a>
          <a href="/readme" className="nav-link">README</a>
          <a href="/contact" className="nav-link">Contact</a>
          {isLoggedIn ? (
            <button onClick={handleLogout} className="btn-primary">Logout</button>
          ) : (
            <a href="/login" className="btn-primary">Login</a>
          )}
        </nav>
        <div className="md:hidden">
          <button onClick={toggleMenu} className="text-primary focus:outline-none">
            <FaBars size={24} />
          </button>
        </div>
      </div>
      {/* Overlay */}
      <div 
        className={`fixed inset-0 bg-black bg-opacity-50 transition-opacity duration-300 ${isMenuOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
        onClick={toggleMenu}
      ></div>
      {/* Sidebar */}
      <div className={`fixed top-0 left-0 h-full bg-secondary w-64 shadow-lg transform transition-transform duration-300 ease-in-out ${isMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="flex justify-end p-4">
          <button onClick={toggleMenu} className="text-primary focus:outline-none">
            <FaTimes size={24} />
          </button>
        </div>
        <nav className="flex flex-col p-4 space-y-4">
          <a href="/" className="nav-link-mobile" onClick={toggleMenu}>Home</a>
          <a href="/agent" className="nav-link-mobile" onClick={toggleMenu}>Agent</a>
          <a href="/readme" className="nav-link-mobile" onClick={toggleMenu}>README</a>
          <a href="/contact" className="nav-link-mobile" onClick={toggleMenu}>Contact</a>
          {isLoggedIn ? (
            <button onClick={handleLogout} className="btn-primary w-full">Logout</button>
          ) : (
            <a href="/login" className="btn-primary text-center" onClick={toggleMenu}>Login</a>
          )}
        </nav>
      </div>
    </header>
  );
}