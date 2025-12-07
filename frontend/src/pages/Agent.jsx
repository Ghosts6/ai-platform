import React, { useState, useMemo } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FiMail, FiBarChart, FiHelpCircle, FiFileText, FiUsers, FiCalendar, FiList, FiSearch, FiPlay } from 'react-icons/fi';
import axios from '../api/axios';
import Swal from 'sweetalert2';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import EmailAgent from '../components/agents/EmailAgent';
import SummarizeAgent from '../components/agents/SummarizeAgent';
import QAAgent from '../components/agents/QAAgent';
import TeamsAgent from '../components/agents/TeamsAgent';
import CalendarAgent from '../components/agents/CalendarAgent';
import ListAgent from '../components/agents/ListAgent';
import ExcelAgent from '../components/agents/ExcelAgent';

const agentComponents = {
  email: EmailAgent,
  summarize: SummarizeAgent,
  qa: QAAgent,
  teams: TeamsAgent,
  calendar: CalendarAgent,
  list: ListAgent,
  excel: ExcelAgent,
};

const allAgents = [
  { id: 'excel', name: 'Excel Agent', icon: FiBarChart, description: 'Analyze data from Excel files.' },
  { id: 'email', name: 'Email Agent', icon: FiMail, description: 'Compose and send emails.' },
  { id: 'summarize', name: 'Summarize Agent', icon: FiFileText, description: 'Summarize long texts.' },
  { id: 'qa', name: 'Q&A Agent', icon: FiHelpCircle, description: 'Answer questions on various topics.' },
  { id: 'teams', name: 'Teams Agent', icon: FiUsers, description: 'Manage team collaboration.' },
  { id: 'calendar', name: 'Calendar Agent', icon: FiCalendar, description: 'Manage calendar events.' },
  { id: 'list', name: 'List Agent', icon: FiList, description: 'Create and manage lists.' },
];

const Agent = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  React.useEffect(() => {
    const state = location.state;
    if (state?.agentId && !selectedAgent) {
      const found = allAgents.find(a => a.id === state.agentId);
      if (found) setSelectedAgent(found);
    }
  }, [location.state, selectedAgent]);

  const filteredAgents = useMemo(() => 
    allAgents.filter(agent => 
      agent.name.toLowerCase().includes(searchTerm.toLowerCase())
    ), [searchTerm]);

  const handleViewHistory = () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    navigate('/agent/history');
  };

  const handleAgentSelect = (agent) => {
    setSelectedAgent(agent);
    setSelectedFile(null);
    setPrompt('');
    setResponse('');
  };

  

  const showError = (error, fallback = 'Error communicating with the agent.') => {
    let msg = fallback;
    if (error?.response?.data?.error) {
      msg = error.response.data.error;
    } else if (typeof error?.message === 'string') {
      msg = error.message;
    }
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: msg,
      background: '#222831',
      color: '#EEEEEE',
      confirmButtonColor: '#00ADB5',
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim() || !selectedAgent) return;

    // Default one-shot flow for other agents
    setIsLoading(true);
    setResponse('');

    try {
      let res;
      if (selectedAgent.id === 'excel' && selectedFile) {
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('agent', 'excel');
        formData.append('file', selectedFile);
        res = await axios.post('/agent/respond/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      } else {
        res = await axios.post('/agent/respond/', { prompt, agent: selectedAgent.id });
      }
      setResponse(res.data.response);
    } catch (error) {
      showError(error);
    }
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col md:flex-row w-full py-8 min-h-screen">
        <aside className="w-full md:w-1/4 md:max-w-xs bg-surface/30 p-4 md:border-r border-primary/20">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-accent/70">Agents</span>
            <button
              onClick={handleViewHistory}
              className="text-xs px-3 py-1 rounded border border-primary/30 text-primary hover:bg-primary/10 transition-colors"
            >
              History
            </button>
          </div>
          <div className="input-icon-group mb-4">
            <span className="icon-element">
              <FiSearch className="text-accent/50 w-5 h-5" />
            </span>
            <input 
              type="text"
              placeholder="Search agents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-background/50 text-accent border-2 border-primary/30 rounded-lg pl-10 pr-3 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300"
            />
          </div>
          <ul className="space-y-2">
            {filteredAgents.map((agent) => (
              <li
                key={agent.id}
                className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all duration-200 ${
                  selectedAgent?.id === agent.id 
                    ? 'bg-primary/20 text-primary shadow-md' 
                    : 'hover:bg-primary/10 hover:translate-x-1'
                }`}
                onClick={() => handleAgentSelect(agent)}
              >
                <agent.icon className="w-5 h-5 flex-shrink-0" />
                <span className="font-medium">{agent.name}</span>
              </li>
            ))}
          </ul>
        </aside>
        <section className="w-full md:w-3/4 p-8 overflow-y-auto">
          {selectedAgent ? (
            <div className="animate-fade-in h-full">
              <h1 className="text-4xl font-display font-extrabold text-primary mb-2">{selectedAgent.name}</h1>
              <p className="text-lg text-accent/80 mb-8">{selectedAgent.description}</p>

              {React.createElement(agentComponents[selectedAgent.id], { selectedAgent, prompt, setPrompt, response, setResponse, isLoading, setIsLoading, handleSubmit })}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <FiHelpCircle className="w-24 h-24 text-primary/20 mb-4" />
              <h2 className="text-3xl font-bold text-accent/80">Select an Agent</h2>
              <p className="text-lg text-accent/60 max-w-md">
                Choose an agent from the list on the left to begin interacting with our specialized AI services.
              </p>
            </div>
          )}
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default Agent;
