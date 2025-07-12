import React from 'react';

export default function Header() {
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
        </nav>
      </div>
    </header>
  );
}