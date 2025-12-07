import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FaBars, FaTimes } from 'react-icons/fa';

export default function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleStorage = () => setIsLoggedIn(!!localStorage.getItem('token'));
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
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

  const isActive = (path) => location.pathname === path;

  return (
    <header className={`w-full bg-secondary text-accent py-4 shadow-lg relative z-50 transition-all duration-300 ${
      isScrolled ? 'shadow-2xl bg-secondary/95 backdrop-blur-sm' : ''
    } sticky top-0`}>
      <div className="container mx-auto flex justify-between items-center px-4 md:px-6 lg:px-8">
        <a href="/" className="flex items-center group transition-transform duration-300 hover:scale-105">
          <span className="logo-icon-wrapper mr-2">
            <img src="/img/logo.png" alt="AIAgent Logo" className="h-10 w-10 md:h-12 md:w-12 transition-transform duration-300 ease-in-out logo-hover" />
          </span>
          <h1 className="text-2xl md:text-3xl font-bold tracking-wide text-primary logo-text-animate">AIAgent</h1>
        </a>
        <nav className="hidden md:flex space-x-6 lg:space-x-8 items-center">
          <a href="/" className={`nav-link ${isActive('/') ? 'nav-link-active' : ''}`}>Home</a>
          <a href="/chatbot" className={`nav-link ${isActive('/chatbot') ? 'nav-link-active' : ''}`}>Chatbot</a>
          <a href="/agents" className={`nav-link ${isActive('/agents') ? 'nav-link-active' : ''}`}>Agents</a>
          <a href="/readme" className={`nav-link ${isActive('/readme') ? 'nav-link-active' : ''}`}>README</a>
          <a href="/contact" className={`nav-link ${isActive('/contact') ? 'nav-link-active' : ''}`}>Contact</a>
          {isLoggedIn ? (
            <button onClick={handleLogout} className="btn-primary ml-2">Logout</button>
          ) : (
            <a href="/login" className="btn-primary ml-2">Login</a>
          )}
        </nav>
        <div className="md:hidden">
          <button 
            onClick={toggleMenu} 
            className="text-primary focus:outline-none p-2 rounded-lg hover:bg-secondary-hover transition-colors duration-200"
            aria-label="Toggle menu"
          >
            <FaBars size={24} />
          </button>
        </div>
      </div>
      {/* Overlay */}
      <div 
        className={`fixed inset-0 bg-black bg-opacity-60 backdrop-blur-sm transition-opacity duration-300 z-40 ${
          isMenuOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={toggleMenu}
      ></div>
      {/* Sidebar */}
      <div className={`fixed top-0 left-0 h-full bg-secondary w-72 shadow-2xl transform transition-transform duration-300 ease-in-out z-50 ${
        isMenuOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex justify-between items-center p-6 border-b border-primary/20">
          <h2 className="text-xl font-bold text-primary">Menu</h2>
          <button 
            onClick={toggleMenu} 
            className="text-primary focus:outline-none p-2 rounded-lg hover:bg-secondary-hover transition-colors duration-200"
            aria-label="Close menu"
          >
            <FaTimes size={24} />
          </button>
        </div>
        <nav className="flex flex-col p-6 space-y-2">
          <a 
            href="/" 
            className={`nav-link-mobile ${isActive('/') ? 'bg-primary text-background' : ''}`} 
            onClick={toggleMenu}
          >
            Home
          </a>
          <a 
            href="/chatbot" 
            className={`nav-link-mobile ${isActive('/chatbot') ? 'bg-primary text-background' : ''}`} 
            onClick={toggleMenu}
          >
            Chatbot
          </a>
          <a 
            href="/agents" 
            className={`nav-link-mobile ${isActive('/agents') ? 'bg-primary text-background' : ''}`} 
            onClick={toggleMenu}
          >
            Agents
          </a>
          <a 
            href="/readme" 
            className={`nav-link-mobile ${isActive('/readme') ? 'bg-primary text-background' : ''}`} 
            onClick={toggleMenu}
          >
            README
          </a>
          <a 
            href="/contact" 
            className={`nav-link-mobile ${isActive('/contact') ? 'bg-primary text-background' : ''}`} 
            onClick={toggleMenu}
          >
            Contact
          </a>
          <div className="pt-4 mt-4 border-t border-primary/20">
            {isLoggedIn ? (
              <button onClick={handleLogout} className="btn-primary w-full">Logout</button>
            ) : (
              <a href="/login" className="btn-primary text-center block w-full" onClick={toggleMenu}>Login</a>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}