import React from 'react';

export default function Footer() {
  return (
    <footer className="w-full bg-secondary text-accent py-3 text-center mt-auto shadow-inner border-t border-primary/30">
      <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-2">
        <div>
          &copy; 2025 AIAgent Platform &mdash; All rights reserved.
        </div>
        <div className="flex flex-col md:flex-row items-center gap-2 text-sm">
          <span>Contact: <a href="mailto:contact@aiagent.com" className="underline hover:text-primary transition">contact@aiagent.com</a></span>
          <span className="hidden md:inline">|</span>
          <span>GitHub: <a href="https://github.com/Ghosts6/ai-platform" target="_blank" rel="noopener noreferrer" className="underline hover:text-primary transition">AIAgent Repo</a></span>
        </div>
      </div>
    </footer>
  );
}