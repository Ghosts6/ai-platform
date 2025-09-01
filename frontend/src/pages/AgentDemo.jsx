import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FiPlay, FiArrowRight, FiZap, FiMail, FiBarChart, FiHelpCircle, FiFileText, FiUsers, FiCalendar, FiList } from 'react-icons/fi';

export default function AgentDemo() {
  const [selectedExample, setSelectedExample] = useState(null);
  const navigate = useNavigate();

  const examples = [
    {
      id: 'email',
      title: 'Email Composition',
      description: 'Help me compose a professional email to schedule a meeting',
      agent: 'Email Agent',
      icon: FiMail,
      prompt: 'Help me compose a professional email to schedule a meeting with a client next week',
      keywords: ['email', 'compose', 'meeting', 'professional']
    },
    {
      id: 'excel',
      title: 'Data Analysis',
      description: 'Analyze this sales data and create a summary report',
      agent: 'Excel Agent',
      icon: FiBarChart,
      prompt: 'I have sales data for Q1-Q4. Can you help me analyze trends and create a summary report?',
      keywords: ['excel', 'data', 'analysis', 'sales', 'report']
    },
    {
      id: 'qa',
      title: 'Question Answering',
      description: 'Get answers to technical questions about our products',
      agent: 'Q&A Agent',
      icon: FiHelpCircle,
      prompt: 'What are the main features of our AI platform and how do they work together?',
      keywords: ['question', 'features', 'platform', 'how']
    },
    {
      id: 'summarize',
      title: 'Content Summarization',
      description: 'Summarize a long document or article',
      agent: 'Summarize Agent',
      icon: FiFileText,
      prompt: 'I have a 20-page technical document. Can you provide a concise summary of the key points?',
      keywords: ['summarize', 'document', 'technical', 'key points']
    },
    {
      id: 'teams',
      title: 'Team Coordination',
      description: 'Schedule team meetings and coordinate tasks',
      agent: 'Teams Agent',
      icon: FiUsers,
      prompt: 'Help me schedule a team meeting for next week and coordinate the agenda items',
      keywords: ['teams', 'meeting', 'schedule', 'coordinate']
    },
    {
      id: 'calendar',
      title: 'Calendar Management',
      description: 'Manage appointments and schedule events',
      agent: 'Calendar Agent',
      icon: FiCalendar,
      prompt: 'I need to schedule several client meetings next month. Can you help me find available time slots?',
      keywords: ['calendar', 'meetings', 'schedule', 'appointments']
    },
    {
      id: 'list',
      title: 'List Organization',
      description: 'Create and manage organized lists',
      agent: 'List Agent',
      icon: FiList,
      prompt: 'Help me create a prioritized task list for our project milestones',
      keywords: ['list', 'tasks', 'prioritize', 'project']
    }
  ];

  const handleExampleSelect = (example) => {
    setSelectedExample(example);
  };

  const startExample = (example) => {
    navigate('/agent', {
      state: {
        agentId: example.id,
        agentName: example.agent,
        initialQuery: example.prompt
      }
    });
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

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="w-full max-w-6xl mx-auto space-y-8">
          {/* Header Section */}
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-4 tracking-tight">
              Agent Demo & Examples
            </h1>
            <p className="text-lg text-accent/80 max-w-2xl mx-auto">
              See how our AI agents work in action. Try these examples or create your own requests.
            </p>
          </div>

          {/* Examples Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {examples.map((example) => {
              const IconComponent = example.icon;
              return (
                <div
                  key={example.id}
                  className={`bg-surface p-6 rounded-xl shadow-lg border-2 transition-all duration-300 cursor-pointer hover:shadow-primary/20 ${
                    selectedExample?.id === example.id 
                      ? 'border-primary shadow-primary/30' 
                      : 'border-transparent hover:border-primary/30'
                  }`}
                  onClick={() => handleExampleSelect(example)}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center">
                      <IconComponent className="w-6 h-6 text-primary" />
                    </div>
                    <span className="text-xs px-2 py-1 bg-primary/20 text-primary rounded-full font-medium">
                      {example.agent}
                    </span>
                  </div>
                  
                  <h3 className="text-xl font-bold text-primary mb-2">{example.title}</h3>
                  <p className="text-accent/70 text-sm mb-4">{example.description}</p>
                  
                  <div className="space-y-3">
                    <div>
                      <h4 className="text-sm font-semibold text-accent/80 mb-2">Example Request:</h4>
                      <p className="text-xs text-accent/60 bg-background/50 p-3 rounded-lg italic">
                        "{example.prompt}"
                      </p>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-semibold text-accent/80 mb-2">Trigger Keywords:</h4>
                      <div className="flex flex-wrap gap-1">
                        {example.keywords.map((keyword, index) => (
                          <span
                            key={index}
                            className="text-xs px-2 py-1 bg-secondary/30 text-accent/60 rounded-full"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Selected Example Action */}
          {selectedExample && (
            <div className="bg-surface/50 backdrop-blur-sm p-6 rounded-xl border border-primary/20">
              <div className="text-center mb-6">
                <h2 className="text-2xl font-bold text-primary mb-2">
                  Try This Example
                </h2>
                <p className="text-accent/80">
                  Experience how the {selectedExample.agent} handles this type of request
                </p>
              </div>
              
              <div className="max-w-3xl mx-auto space-y-4">
                <div className="bg-background/50 p-4 rounded-lg">
                  <h3 className="font-semibold text-primary mb-2">Your Request:</h3>
                  <p className="text-accent/80">"{selectedExample.prompt}"</p>
                </div>
                
                <div className="bg-background/50 p-4 rounded-lg">
                  <h3 className="font-semibold text-primary mb-2">How It Works:</h3>
                  <div className="flex items-center justify-center gap-4 text-sm text-accent/70">
                    <span>1. Request sent to {selectedExample.agent}</span>
                    <FiArrowRight className="w-4 h-4" />
                    <span>2. Agent processes your request</span>
                    <FiArrowRight className="w-4 h-4" />
                    <span>3. Get specialized response</span>
                  </div>
                </div>
                
                <div className="flex justify-center">
                  <button
                    onClick={() => startExample(selectedExample)}
                    className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-hover transition-colors duration-300 flex items-center gap-2"
                  >
                    <FiPlay className="w-4 h-4" />
                    Try This Example
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* General Chat Section */}
          <div className="bg-gradient-to-r from-primary/10 to-secondary/10 p-6 rounded-xl border border-primary/20">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-primary mb-4">
                <FiZap className="inline-block w-6 h-6 mr-2" />
                Try Your Own Request
              </h2>
              <p className="text-accent/80 mb-6 max-w-2xl mx-auto">
                Don't see an example that fits your needs? Start a general chat and let our AI manager automatically route your request to the best agent.
              </p>
              <button
                onClick={startGeneralChat}
                className="bg-gradient-to-r from-primary to-primary-hover text-white font-bold py-3 px-8 rounded-lg hover:from-primary-hover hover:to-primary transition-all duration-300 shadow-lg hover:shadow-primary/25 transform hover:scale-105 flex items-center gap-2 mx-auto"
              >
                Start General Chat
              </button>
            </div>
          </div>

          {/* How It Works Section */}
          <div className="bg-surface/30 p-6 rounded-xl border border-primary/20">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold text-primary mb-4">
                How Our Agent System Works
              </h2>
            </div>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">1</span>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">Input</h3>
                <p className="text-accent/70 text-sm">Type your request in natural language</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">2</span>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">Analysis</h3>
                <p className="text-accent/70 text-sm">AI analyzes keywords and context</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">3</span>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">Routing</h3>
                <p className="text-accent/70 text-sm">Request routed to best agent</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary">4</span>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">Response</h3>
                <p className="text-accent/70 text-sm">Get specialized assistance</p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
} 