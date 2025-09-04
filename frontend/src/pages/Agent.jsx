import React, { useState, useMemo } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import FileUpload from '../components/FileUpload';
import { FiMail, FiBarChart, FiHelpCircle, FiFileText, FiUsers, FiCalendar, FiList, FiSearch, FiPlay } from 'react-icons/fi';
import axios from '../api/axios';
import Swal from 'sweetalert2';
import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

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
  const [excelMessages, setExcelMessages] = useState([]); // {sender: 'user'|'agent', text: string}
  const [excelSessionId, setExcelSessionId] = useState(null);
  const [excelTyping, setExcelTyping] = useState(false);
  const chatEndRef = React.useRef(null);
  React.useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [excelMessages, excelTyping, selectedAgent]);

  React.useEffect(() => {
    const state = location.state;
    if (state?.agentId && !selectedAgent) {
      const found = allAgents.find(a => a.id === state.agentId);
      if (found) setSelectedAgent(found);
    }
  }, [location.state, selectedAgent]);

  React.useEffect(() => {
    const state = location.state;
    const sessionId = state?.sessionId;
    if (!sessionId) return;
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    const fetchSession = async () => {
      try {
        const res = await axios.get(`/core/chat/session/${sessionId}/`, {
          headers: { Authorization: `Token ${token}` }
        });
        const msgs = res.data || [];
        // If Excel agent, hydrate excelMessages
        if (selectedAgent?.id === 'excel') {
          const transformed = msgs.map(m => ({ sender: m.sender, text: m.text }));
          setExcelMessages(transformed);
          setExcelSessionId(sessionId);
        }
      } catch (e) {
        // ignore, handled by auth interceptor if 401
      }
    };
    fetchSession();
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
    if (agent.id === 'excel') {
      setExcelMessages([]);
      setExcelSessionId(null);
      setExcelTyping(false);
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      Swal.fire({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 1200,
        background: '#222831',
        color: '#EEEEEE',
        icon: 'success',
        title: 'Copied',
      });
    } catch {}
  };

  const handleKeyDown = (e) => {
    if (selectedAgent?.id === 'excel') {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (prompt.trim()) {
          const fakeEvent = { preventDefault: () => {} };
          handleSubmit(fakeEvent);
        }
      }
    }
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

    // Excel agent uses chat-style flow
    if (selectedAgent.id === 'excel') {
      const userMsg = { sender: 'user', text: prompt };
      setExcelMessages(prev => [...prev, userMsg]);
      setExcelTyping(true);
      setPrompt('');
      try {
        let res;
        if (selectedFile) {
          const formData = new FormData();
          formData.append('prompt', userMsg.text);
          formData.append('agent', 'excel');
          if (excelSessionId) formData.append('session_id', excelSessionId);
          formData.append('file', selectedFile);
          res = await axios.post('/agent/respond/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
        } else {
          const payload = { prompt: userMsg.text, agent: 'excel' };
          if (excelSessionId) payload.session_id = excelSessionId;
          res = await axios.post('/agent/respond/', payload);
        }
        const agentText = res.data.response;
        const newSessionId = res.data.session_id || excelSessionId;
        if (newSessionId && newSessionId !== excelSessionId) setExcelSessionId(newSessionId);
        setExcelMessages(prev => [...prev, { sender: 'agent', text: agentText }]);
      } catch (error) {
        showError(error, 'Error communicating with the Excel agent.');
      }
      setExcelTyping(false);
      return;
    }

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
      <main className="flex-1 flex w-full">
        <aside className="w-1/4 max-w-xs bg-surface/30 p-4 border-r border-primary/20">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-accent/70">Agents</span>
            <button
              onClick={handleViewHistory}
              className="text-xs px-3 py-1 rounded border border-primary/30 text-primary hover:bg-primary/10 transition-colors"
            >
              History
            </button>
          </div>
          <div className="relative mb-4">
            <FiSearch className="absolute top-3 left-3 text-accent/50" />
            <input 
              type="text"
              placeholder="Search agents..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-background/50 text-accent border-2 border-primary/30 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300"
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
        <section className="w-3/4 p-8 overflow-y-auto">
          {selectedAgent ? (
            <div className="animate-fade-in">
              <h1 className="text-4xl font-display font-extrabold text-primary mb-2">{selectedAgent.name}</h1>
              <p className="text-lg text-accent/80 mb-8">{selectedAgent.description}</p>

              {/* Excel agent chat UI */}
              {selectedAgent.id === 'excel' ? (
                <div>
                  <div className="mb-4 p-4 bg-surface/50 rounded-xl border border-primary/20">
                    <FileUpload onFileChange={handleFileChange} selectedFile={selectedFile} />
                    {selectedFile && (
                      <div className="mt-2 text-sm text-accent/70">Selected file: {selectedFile.name}</div>
                    )}
                  </div>

                  <div className="flex flex-col gap-3 max-h-[50vh] overflow-y-auto p-4 bg-background/50 rounded-xl border border-primary/20">
                    {excelMessages.length === 0 && (
                      <div className="text-accent/60 text-sm">
                        Start by uploading a file (CSV, TSV, JSON, XLS/XLSX) and ask things like "describe", "head", "columns", "rows", or "convert to xlsx".
                      </div>
                    )}
                    {excelMessages.map((m, idx) => (
                      <div key={idx} className={`max-w-[80%] p-3 rounded-lg ${m.sender === 'user' ? 'self-end bg-primary text-white' : 'self-start bg-surface/70 border border-primary/20'}`}>
                        <pre className={`whitespace-pre-wrap font-sans text-sm ${m.sender === 'user' ? 'text-white' : 'text-accent/90'}`}>{m.text}</pre>
                        <div className="flex justify-end mt-1">
                          <button
                            onClick={() => copyToClipboard(m.text)}
                            className="text-accent/50 hover:text-accent transition-colors"
                            title="Copy"
                          >
                            <FiPlay className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                    {excelTyping && (
                      <div className="self-start max-w-[60%] p-3 rounded-lg bg-surface/70 border border-primary/20 text-accent/70 text-sm">
                        Typing...
                      </div>
                    )}
                    <div ref={chatEndRef} />
                  </div>

                  <form onSubmit={handleSubmit} className="mt-4 flex gap-3">
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder={`Message ${selectedAgent.name}...`}
                      className="flex-1 bg-surface/50 text-accent border-2 border-primary/30 rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300 h-24 resize-none"
                    />
                    <button
                      type="submit"
                      disabled={!prompt.trim()}
                      className="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-hover transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-primary/25"
                    >
                      <FiPlay className="w-5 h-5" />
                      Send
                    </button>
                  </form>
                </div>
              ) : (
                // Default UI for other agents
                <form onSubmit={handleSubmit}>
                  <div className="mb-4">
                    <textarea
                      value={prompt}
                      onChange={(e) => setPrompt(e.target.value)}
                      placeholder={`What should I ask the ${selectedAgent.name}?`}
                      className="w-full bg-surface/50 text-accent border-2 border-primary/30 rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300 h-40 resize-none"
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isLoading || !prompt.trim()}
                    className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-hover transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-primary/25 transform hover:scale-105"
                  >
                    {isLoading ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                        Processing...
                      </>
                    ) : (
                      <>
                        <FiPlay className="w-5 h-5" />
                        Submit to Agent
                      </>
                    )}
                  </button>

                  {response && (
                    <div className="mt-8 p-6 bg-surface/50 rounded-xl border border-primary/20 animate-fade-in">
                      <h3 className="text-2xl font-bold text-primary mb-4">Agent Response</h3>
                      <div className="bg-background/50 p-4 rounded-lg">
                        <pre className="whitespace-pre-wrap text-accent/80 font-mono text-sm">{response}</pre>
                      </div>
                    </div>
                  )}
                </form>
              )}
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
