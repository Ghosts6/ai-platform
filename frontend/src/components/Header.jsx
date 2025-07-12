import React from 'react';

export default function Header() {
  return (
    <header className="w-full bg-primary text-white py-4 shadow">
      <div className="container mx-auto flex justify-between items-center px-4">
        <h1 className="text-2xl font-bold tracking-wide">AIAgent Platform</h1>
        <nav className="space-x-4 flex items-center">
          <a href="/" className="hover:underline transition-colors px-2 py-1 rounded-lg hover:bg-gold/20 active:bg-gold/40 focus:outline-none focus:ring-2 focus:ring-gold">Home</a>
          <a href="/agent" className="hover:underline transition-colors px-2 py-1 rounded-lg hover:bg-gold/20 active:bg-gold/40 focus:outline-none focus:ring-2 focus:ring-gold">Agent</a>
          <a href="/readme" className="hover:underline transition-colors px-2 py-1 rounded-lg hover:bg-gold/20 active:bg-gold/40 focus:outline-none focus:ring-2 focus:ring-gold">README</a>
          <a href="/contact" className="hover:underline transition-colors px-2 py-1 rounded-lg hover:bg-gold/20 active:bg-gold/40 focus:outline-none focus:ring-2 focus:ring-gold">Contact</a>
        </nav>
      </div>
    </header>
  );
}
