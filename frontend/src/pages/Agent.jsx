import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaUserSecret, FaRobot, FaCogs } from 'react-icons/fa';

export default function Agent() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="w-full max-w-4xl mx-auto bg-surface rounded-2xl shadow-2xl p-8 animate-fadeIn">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight flex items-center justify-center gap-3">
              <FaRobot className="text-primary animate-bounce" /> Agent Management
            </h1>
            <p className="text-lg text-accent/80">
              Manage your AI agents, view their status, and configure new workflows.
            </p>
          </div>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-background p-6 rounded-lg shadow-lg hover:shadow-primary/50 transition-shadow duration-300">
              <div className="flex items-center gap-4 mb-4">
                <FaUserSecret className="text-primary text-3xl" />
                <h2 className="text-2xl font-bold">Create New Agent</h2>
              </div>
              <p className="text-accent/80">Create a new agent from scratch and define its personality and capabilities.</p>
              <button className="mt-4 w-full">Create Agent</button>
            </div>
            <div className="bg-background p-6 rounded-lg shadow-lg hover:shadow-primary/50 transition-shadow duration-300">
              <div className="flex items-center gap-4 mb-4">
                <FaCogs className="text-primary text-3xl" />
                <h2 className="text-2xl font-bold">Configure Workflows</h2>
              </div>
              <p className="text-accent/80">Define complex workflows and connect multiple agents to automate tasks.</p>
              <button className="mt-4 w-full">Configure</button>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
