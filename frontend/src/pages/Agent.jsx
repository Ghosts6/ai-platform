import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaUserSecret, FaRobot, FaCogs } from 'react-icons/fa';

export default function Agent() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="flex flex-col items-center gap-6 max-w-xl w-full bg-white/90 rounded-xl shadow-xl p-8 animate-fadeIn">
          <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight text-center flex items-center gap-2">
            <FaRobot className="text-gold animate-bounce" /> Agent Management
          </h1>
          <p className="text-lg text-accent/80 text-center mb-4">
            Manage your AI agents, view their status, and configure new workflows.
          </p>
          <div className="flex flex-col gap-4 w-full">
            <div className="flex items-center gap-3 text-lg group">
              <FaUserSecret className="text-gold group-hover:scale-110 transition-transform duration-200" />
              <span className="font-semibold group-hover:text-gold transition-colors">Create New Agent</span>
            </div>
            <div className="flex items-center gap-3 text-lg group">
              <FaCogs className="text-gold group-hover:rotate-12 transition-transform duration-200" />
              <span className="font-semibold group-hover:text-gold transition-colors">Configure Workflows</span>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
