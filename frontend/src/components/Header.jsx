import React, { useState } from 'react';
import { FaUserCircle } from 'react-icons/fa';

export default function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('Kiarash'); // Simulated username

  return (
    <header className="w-full bg-secondary text-accent py-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center px-4">
        <a href="/" className="flex items-center gap-3 group">
          <img src="/img/logo.png" alt="AIAgent Logo" className="h-8 w-8 transition-transform duration-300 ease-in-out group-hover:scale-110 group-active:scale-95" />
          <h1 className="text-2xl font-bold tracking-wide text-primary">AIAgent</h1>
        </a>
        <nav className="space-x-4 flex items-center">
          <a href="/" className="nav-link">Home</a>
          <a href="/agent" className="nav-link">Agent</a>
          <a href="/readme" className="nav-link">README</a>
          <a href="/contact" className="nav-link">Contact</a>
          {isLoggedIn ? (
            <div className="relative group">
              <FaUserCircle className="text-3xl text-primary cursor-pointer" />
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="px-4 py-2 text-gray-800">{username}</div>
                <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Logout</a>
              </div>
            </div>
          ) : (
            <a href="/login" className="login-button-header">Login</a>
          )}
        </nav>
      </div>
    </header>
  );
}