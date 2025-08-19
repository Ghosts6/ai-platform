import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

export default function Agents() {
  const [selectedAgent, setSelectedAgent] = useState('');
  const [agents, setAgents] = useState([
    { id: '1', name: 'Calendar Agent' },
    { id: '2', name: 'Email Agent' },
    { id: '3', name: 'Excel Agent' },
    { id: '4', name: 'QA Agent' },
  ]); // Placeholder for agents, will be fetched from API

  const handleAgentChange = (event) => {
    const agentId = event.target.value;
    setSelectedAgent(agentId);
    if (agentId) {
      startAgentInteraction(agentId);
    }
  };

  const startAgentInteraction = (agentId) => {
    console.log(`Starting interaction with agent: ${agentId}`);
    // Later: fetch agent details or navigate to specific chat page
  };

  // useEffect(() => {
  //   // Fetch agents from API here
  //   // Example: axios.get('/api/agents').then(response => setAgents(response.data));
  // }, []);

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="w-full max-w-4xl mx-auto bg-surface rounded-2xl shadow-2xl p-8 animate-fadeIn">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight">
              AI Agents
            </h1>
            <p className="text-lg text-accent/80">
              Explore and interact with various specialized AI agents.
            </p>
          </div>

          {/* Two-column grid */}
          <div className="grid md:grid-cols-2 gap-8">
            {/* Select Agent card */}
            <div className="bg-background p-6 rounded-lg shadow-lg hover:shadow-primary/50 transition-shadow duration-300 text-center">
              <h2 className="text-2xl font-bold text-primary mb-4">
                Select Specific Agent
              </h2>
              <p className="text-accent/80 mb-6">
                Choose from a list of specialized AI agents for specific tasks.
              </p>
              <div className="relative">
                <select
                  className="appearance-none w-full bg-surface text-accent py-2 px-4 rounded border-2 border-primary/30 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300 cursor-pointer text-center pr-8"
                  value={selectedAgent}
                  onChange={handleAgentChange}
                >
                  <option value="">-- Select an Agent --</option>
                  {agents.map((agent) => (
                    <option
                      key={agent.id}
                      value={agent.id}
                    >
                      {agent.name}
                    </option>
                  ))}
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-white">
                  <svg
                    className="fill-current h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Agent Manager card */}
            <div className="bg-background p-6 rounded-lg shadow-lg hover:shadow-primary/50 transition-shadow duration-300 text-center">
              <h2 className="text-2xl font-bold text-primary mb-4">
                Let Agent Manager Decide
              </h2>
              <p className="text-accent/80 mb-6">
                Enter your query and let the AI manager route it to the best agent.
              </p>
              <button className="w-full bg-primary text-white font-bold py-2 px-4 rounded hover:bg-primary/80 transition-colors duration-300">
                Start General Chat
              </button>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
