import React from 'react';
import { FaEnvelope, FaGithub } from 'react-icons/fa';

export default function Footer() {
  return (
    <footer className="w-full bg-secondary text-accent py-5 text-center mt-auto shadow-inner border-t border-primary/30 transition-colors duration-300 hover:bg-secondary/50">
      <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2 text-lg font-semibold">
          <span className="text-primary">&copy; 2025</span>
          <span>AIAgent Platform</span>
        </div>
        <div className="flex items-center gap-4 text-base md:text-lg">
          <a href="mailto:contact@aiagent.com" className="flex items-center gap-1 underline hover:text-primary active:scale-95 transition font-semibold" title="Email us">
            <FaEnvelope className="text-primary" /> contact@aiagent.com
          </a>
          <span className="hidden md:inline text-accent/50">|</span>
          <a href="https://github.com/Ghosts6/ai-platform" target="_blank" rel="noopener noreferrer" className="flex items-center gap-1 underline hover:text-primary active:scale-95 transition font-semibold" title="GitHub Repository">
            <FaGithub className="text-primary" /> GitHub
          </a>
        </div>
      </div>
    </footer>
  );
}