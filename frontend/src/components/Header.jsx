import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FaBars, FaTimes, FaHome, FaComments, FaUsers, FaBook, FaEnvelope, FaSignInAlt, FaSignOutAlt } from 'react-icons/fa';

const NavLinks = ({ navItems, handleNavClick, isActive, isMobile }) => {
  return (
    <>
      {navItems.map((item, index) => (
        <a
          key={item.path}
          href={item.path}
          onClick={(e) => handleNavClick(e, item.path)}
          className={`relative font-medium transition-all duration-300 flex items-center gap-2 group ${
            isMobile
              ? `px-4 py-3.5 rounded-lg ${isActive(item.path) ? 'bg-primary text-background shadow-lg shadow-primary/20 scale-[1.02]' : 'text-accent hover:bg-primary/10 hover:text-primary hover:translate-x-1'}`
              : `px-4 py-2 rounded-lg ${isActive(item.path) ? 'text-primary' : 'text-accent/80 hover:text-primary'}`
          }`}
          style={{ animationDelay: isMobile ? `${index * 50}ms` : '0ms' }}
        >
          <item.icon className={`w-4 h-4 transition-transform duration-300 ${isActive(item.path) ? 'scale-110' : 'group-hover:scale-110'}`} />
          <span>{item.label}</span>
          {!isMobile && isActive(item.path) && (
            <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-12 h-0.5 bg-primary rounded-full"></span>
          )}
          {!isMobile && !isActive(item.path) && (
            <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0.5 bg-primary rounded-full transition-all duration-300 group-hover:w-12"></span>
          )}
          {isMobile && isActive(item.path) && (
            <div className="ml-auto w-2 h-2 bg-background rounded-full"></div>
          )}
        </a>
      ))}
    </>
  );
};

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

  const handleNavClick = (e, path) => {
    e.preventDefault();
    setIsMenuOpen(false);
    navigate(path);
  };

  const navItems = [
    { path: '/', label: 'Home', icon: FaHome },
    { path: '/chatbot', label: 'Chatbot', icon: FaComments },
    { path: '/agents', label: 'Agents', icon: FaUsers },
    { path: '/readme', label: 'README', icon: FaBook },
    { path: '/contact', label: 'Contact', icon: FaEnvelope },
  ];

  return (
    <>
      <header className={`w-full bg-secondary/95 backdrop-blur-md text-accent py-3 md:py-4 shadow-lg fixed top-0 z-50 transition-all duration-300 border-b border-primary/10 ${
        isScrolled ? 'shadow-2xl bg-secondary/98' : ''
      }`}>
        <div className="container mx-auto flex justify-between items-center gap-4 px-4 md:px-6">
          {/* Logo */}
          <a
            href="/"
            onClick={(e) => handleNavClick(e, '/')}
            className="flex items-center gap-3 group relative"
          >
            <div className="relative">
              <div className="absolute inset-0 bg-primary/20 rounded-full blur-md group-hover:blur-lg transition-all duration-300"></div>
              <img
                src="/img/logo.png"
                alt="AIAgent Logo"
                className="h-10 w-10 md:h-12 md:w-12 relative z-10 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-6"
              />
            </div>
            <div className="flex flex-col">
              <h1 className="text-xl md:text-2xl font-bold tracking-tight text-primary transition-all duration-300 group-hover:text-primary-hover">
                AIAgent
              </h1>
              <span className="text-xs text-accent/60 font-medium">Smart Solutions</span>
            </div>
          </a>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            <NavLinks navItems={navItems} handleNavClick={handleNavClick} isActive={isActive} isMobile={false} />
          </nav>

          {/* Auth Button Desktop */}
          <div className="hidden md:flex items-center gap-3">
            {isLoggedIn ? (
              <button
                onClick={handleLogout}
                className="px-5 py-2.5 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg font-semibold flex items-center gap-2 shadow-lg shadow-red-500/20 hover:shadow-red-500/40 transition-all duration-300 hover:scale-105 active:scale-95"
              >
                <FaSignOutAlt className="w-4 h-4" />
                <span>Logout</span>
              </button>
            ) : (
              <a
                href="/login"
                onClick={(e) => handleNavClick(e, '/login')}
                className="px-5 py-2.5 bg-gradient-to-r from-primary to-primary-hover text-background rounded-lg font-semibold flex items-center gap-2 shadow-lg shadow-primary/20 hover:shadow-primary/40 transition-all duration-300 hover:scale-105 active:scale-95"
              >
                <FaSignInAlt className="w-4 h-4" />
                <span>Login</span>
              </a>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={toggleMenu}
            className="md:hidden p-2.5 rounded-lg text-primary hover:bg-primary/10 transition-all duration-300 active:scale-95"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>
      </header>

      {/* Spacer to prevent content jump */}
      <div className="h-16 md:h-20"></div>

      {/* Mobile Menu Overlay */}
      <div
        className={`fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity duration-300 z-40 lg:hidden ${
          isMenuOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={toggleMenu}
      ></div>

      {/* Mobile Sidebar */}
      <div className={`fixed top-0 right-0 h-full bg-secondary w-80 shadow-2xl transform transition-transform duration-300 ease-out z-50 lg:hidden ${
        isMenuOpen ? 'translate-x-0' : 'translate-x-full'
      }`}>
        {/* Sidebar Header */}
        <div className="flex justify-between items-center p-6 border-b border-primary/20 bg-gradient-to-r from-primary/10 to-transparent">
          <div className="flex items-center gap-3">
            <img src="/img/logo.png" alt="AIAgent" className="h-10 w-10" />
            <div>
              <h2 className="text-lg font-bold text-primary">AIAgent</h2>
              <span className="text-xs text-accent/60">Navigation</span>
            </div>
          </div>
          <button
            onClick={toggleMenu}
            className="p-2 rounded-lg text-primary hover:bg-primary/10 transition-all duration-300 active:scale-95"
            aria-label="Close menu"
          >
            <FaTimes size={22} />
          </button>
        </div>

        {/* Sidebar Navigation */}
        <nav className="flex flex-col p-4 space-y-1 overflow-y-auto h-[calc(100%-160px)]">
          <NavLinks navItems={navItems} handleNavClick={handleNavClick} isActive={isActive} isMobile={true} />
        </nav>

        {/* Sidebar Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-primary/20 bg-gradient-to-t from-secondary/50 to-transparent">
          {isLoggedIn ? (
            <button
              onClick={handleLogout}
              className="w-full px-5 py-3.5 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg font-semibold flex items-center justify-center gap-2 shadow-lg shadow-red-500/20 hover:shadow-red-500/40 transition-all duration-300 hover:scale-[1.02] active:scale-95"
            >
              <FaSignOutAlt className="w-5 h-5" />
              <span>Logout</span>
            </button>
          ) : (
            <a
              href="/login"
              onClick={(e) => handleNavClick(e, '/login')}
              className="btn-secondary w-full flex items-center justify-center"
            >
              <FaSignInAlt className="w-5 h-5" />
              <span>Login</span>
            </a>
          )}
        </div>
      </div>
    </>
  );
}