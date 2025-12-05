import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/axios';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ScrollToTopButton from '../components/ScrollToTopButton';
import { FiZap, FiMessageCircle, FiPlay, FiInfo, FiMail, FiFileText, FiHelpCircle, FiBarChart, FiUsers, FiCalendar, FiList } from 'react-icons/fi';

export default function Agents() {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userQuery, setUserQuery] = useState('');
  const [isQueryLoading, setIsQueryLoading] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const navigate = useNavigate();
  const interactionRef = useRef(null);

  // Agent definitions based on your backend agent system
  const agentDefinitions = {
    'email': {
      name: 'Email Agent',
      description: 'Specialized in email composition, analysis, and management tasks',
      capabilities: ['Email composition', 'Email analysis', 'Email scheduling', 'Email templates', 'Microsoft 365 integration'],
      status: 'active',
      icon: FiMail,
      keywords: ['email', 'inbox', 'mail', 'draft', 'analyze', 'reply', 'send', 'compose', 'attachment']
    },
    'excel': {
      name: 'Excel Agent',
      description: 'Handles Excel file operations, data analysis, and spreadsheet tasks',
      capabilities: ['Data analysis', 'Spreadsheet operations', 'Chart generation', 'Data cleaning', 'CSV processing'],
      status: 'active',
      icon: FiBarChart,
      keywords: ['excel', 'spreadsheet', 'sheet', 'analyze', 'table', 'csv', 'cell', 'formula']
    },
    'qa': {
      name: 'Q&A Agent',
      description: 'Answers questions and provides information on various topics',
      capabilities: ['Question answering', 'Information retrieval', 'Knowledge synthesis', 'Fact checking'],
      status: 'active',
      icon: FiHelpCircle,
      keywords: ['ask', 'answer:', 'list qas', 'delete ', 'update ']
    },
    'summarize': {
      name: 'Summarize Agent',
      description: 'Creates concise summaries of documents, articles, and content',
      capabilities: ['Text summarization', 'Content extraction', 'Key point identification', 'Document analysis'],
      status: 'active',
      icon: FiFileText,
      keywords: ['summarize', 'summary']
    },
    'teams': {
      name: 'Teams Agent',
      description: 'Manages team collaboration, scheduling, and communication tasks',
      capabilities: ['Team scheduling', 'Meeting coordination', 'Task management', 'Communication', 'Maintenance surveys'],
      status: 'active',
      icon: FiUsers,
      keywords: ['teams', 'maintenance', 'survey', 'test running']
    },
    'calendar': {
      name: 'Calendar Agent',
      description: 'Manages calendar events, meetings, and scheduling',
      capabilities: ['Event scheduling', 'Meeting coordination', 'Appointment management', 'Calendar integration'],
      status: 'active',
      icon: FiCalendar,
      keywords: ['calendar', 'event', 'meeting', 'appointment']
    },
    'list': {
      name: 'List Agent',
      description: 'Creates, manages, and organizes lists and structured data',
      capabilities: ['List creation', 'Data organization', 'Task lists', 'Inventory management'],
      status: 'active',
      icon: FiList,
      keywords: ['list', 'organize', 'create list', 'manage list']
    }
  };

  useEffect(() => {
    // Convert agent definitions to the format expected by the component
    const agentsList = Object.entries(agentDefinitions).map(([key, agent]) => ({
      id: key,
      ...agent,
      iconComponent: agent.icon
    }));
    setAgents(agentsList);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };
    window.addEventListener('scroll', toggleVisibility);
    return () => window.removeEventListener('scroll', toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleAgentSelect = (agent) => {
    navigate('/agent', { state: { agentId: agent.id, agentName: agent.name } });
  };

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!userQuery.trim() || !selectedAgent) return;

    setIsQueryLoading(true);
    try {
      // Navigate to agent with the selected agent
      navigate('/agent', { 
        state: { 
          agentId: selectedAgent.id,
          agentName: selectedAgent.name,
          initialQuery: userQuery 
        }
      });
    } catch (err) {
      console.error('Error starting agent interaction:', err);
    } finally {
      setIsQueryLoading(false);
    }
  };

  const startGeneralChat = () => {
    navigate('/chatbot/new', { 
      state: { 
        agentId: 'general',
        agentName: 'AI Manager',
        initialQuery: ''
      }
    });
  };

  const handleViewHistory = () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    navigate('/agent/history');
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-500';
      case 'inactive': return 'text-gray-500';
      case 'error': return 'text-red-500';
      case 'processing': return 'text-yellow-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active': return '🟢';
      case 'inactive': return '⚪️';
      case 'error': return '🔴';
      case 'processing': return '🟡';
      default: return '⚪️';
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col min-h-screen bg-background text-accent font-body">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-lg text-accent/80">Loading agents...</p>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="w-full max-w-6xl mx-auto space-y-8">
          {/* Header Section */}
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight">
              AI Agents
            </h1>
            <p className="text-lg text-accent/80 max-w-2xl mx-auto mb-4">
              Explore and interact with specialized AI agents designed to handle specific tasks and workflows.
            </p>
            <div className="flex items-center justify-center gap-3">
              <button
                onClick={handleViewHistory}
                className="px-5 py-2 rounded-lg border border-primary/30 text-primary hover:bg-primary/10 transition-colors"
              >
                View History
              </button>
            </div>
          </div>

          {/* Agent Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => {
              const IconComponent = agent.iconComponent;
              return (
                <div
                  key={agent.id}
                  className={`bg-surface p-6 rounded-xl shadow-lg border-2 transition-all duration-300 cursor-pointer hover:shadow-primary/20 ${
                    selectedAgent?.id === agent.id 
                      ? 'border-primary shadow-primary/30' 
                      : 'border-transparent hover:border-primary/30'
                  }`}
                  onClick={() => handleAgentSelect(agent)}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center">
                      <IconComponent className="w-6 h-6 text-primary" />
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`text-sm ${getStatusColor(agent.status)}`}>
                        {getStatusIcon(agent.status)}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        agent.status === 'active' ? 'bg-green-500/20 text-green-400' :
                        agent.status === 'inactive' ? 'bg-gray-500/20 text-gray-400' :
                        agent.status === 'error' ? 'bg-red-500/20 text-red-400' :
                        'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {agent.status}
                      </span>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-bold text-primary mb-2">{agent.name}</h3>
                  <p className="text-accent/70 text-sm mb-4">{agent.description}</p>
                  
                  <div className="space-y-2">
                    <h4 className="text-sm font-semibold text-accent/80">Capabilities:</h4>
                    <div className="flex flex-wrap gap-1">
                      {agent.capabilities.slice(0, 3).map((capability, index) => (
                        <span
                          key={index}
                          className="text-xs px-2 py-1 bg-primary/20 text-primary rounded-full"
                        >
                          {capability}
                        </span>
                      ))}
                      {agent.capabilities.length > 3 && (
                        <span className="text-xs px-2 py-1 bg-secondary/50 text-accent/70 rounded-full">
                          +{agent.capabilities.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-primary/10">
                    <h4 className="text-xs font-semibold text-accent/60 mb-2">Trigger Keywords:</h4>
                    <div className="flex flex-wrap gap-1">
                      {agent.keywords.slice(0, 3).map((keyword, index) => (
                        <span
                          key={index}
                          className="text-xs px-2 py-1 bg-secondary/30 text-accent/60 rounded-full"
                        >
                          {keyword}
                        </span>
                      ))}
                      {agent.keywords.length > 3 && (
                        <span className="text-xs px-2 py-1 bg-secondary/20 text-accent/50 rounded-full">
                          +{agent.keywords.length - 3}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Interaction Section */}
          {selectedAgent && (
            <div ref={interactionRef} className="bg-surface/50 backdrop-blur-sm p-6 rounded-xl border border-primary/20">
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-primary mb-2">
                  Interact with {selectedAgent.name}
                </h2>
                <p className="text-accent/80">
                  Ask a question or describe what you need help with. This agent specializes in {selectedAgent.description.toLowerCase()}
                </p>
              </div>
              
              <form onSubmit={handleQuerySubmit} className="max-w-2xl mx-auto">
                <div className="flex gap-4">
                  <input
                    type="text"
                    value={userQuery}
                    onChange={(e) => setUserQuery(e.target.value)}
                    placeholder={`Ask ${selectedAgent.name} anything...`}
                    className="flex-1 bg-background text-accent border-2 border-primary/30 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300"
                  />
                  <button
                    type="submit"
                    disabled={!userQuery.trim() || isQueryLoading}
                    className="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-hover transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                  >
                    {isQueryLoading ? (
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    ) : (
                      <FiPlay className="w-4 h-4" />
                    )}
                    Start Chat
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* General Chat Section */}
          <div className="bg-gradient-to-r from-primary/10 to-secondary/10 p-6 rounded-xl border border-primary/20">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-primary mb-4">
                <FiZap className="inline-block w-6 h-6 mr-2" />
                Let AI Manager Decide
              </h2>
              <p className="text-accent/80 mb-6 max-w-2xl mx-auto">
                Not sure which agent to use? Our intelligent routing system will automatically detect the best agent for your request based on keywords and context.
              </p>
              <div className="flex gap-3 justify-center mb-4">
                <button
                  onClick={() => navigate('/agent')}
                  className="px-5 py-3 rounded-lg border border-primary/30 text-primary hover:bg-primary/10 transition-colors"
                >
                  Open Agent Workspace
                </button>
              </div>
              <button
                onClick={startGeneralChat}
                className="bg-gradient-to-r from-primary to-primary-hover text-white font-bold py-3 px-8 rounded-lg hover:from-primary-hover hover:to-primary transition-all duration-300 shadow-lg hover:shadow-primary/25 transform hover:scale-105 flex items-center gap-2 mx-auto"
              >
                <FiMessageCircle className="w-5 h-5" />
                Start General Chat
              </button>
            </div>
          </div>

          {/* How It Works Section */}
          <div className="bg-surface/30 p-6 rounded-xl border border-primary/20">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold text-primary mb-4">
                <FiInfo className="inline-block w-6 h-6 mr-2" />
                How It Works
              </h2>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">1</span>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">Type Your Request</h3>
                <p className="text-accent/70 text-sm">Simply describe what you need help with in natural language</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">2</span>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">Smart Routing</h3>
                <p className="text-accent/70 text-sm">Our AI automatically detects the best agent for your task</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">3</span>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">Get Results</h3>
                <p className="text-accent/70 text-sm">Receive specialized assistance from the most appropriate agent</p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
      <ScrollToTopButton visible={isVisible} onClick={scrollToTop} />
    </div>
  );
}
