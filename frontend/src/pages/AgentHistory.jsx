import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/axios';
import Header from '../components/Header';
import Footer from '../components/Footer';
import Swal from 'sweetalert2';
import { FaHistory, FaComments, FaTimesCircle } from 'react-icons/fa';

const inferAgentFromSession = (session) => {
  // Best-effort: look at first agent message content prefixes
  const agentMsg = session.messages?.find(m => m.sender === 'agent');
  const text = (agentMsg?.text || '').toLowerCase();
  if (text.includes('excelagent')) return { id: 'excel', name: 'Excel Agent' };
  if (text.includes('email')) return { id: 'email', name: 'Email Agent' };
  if (text.includes('teams')) return { id: 'teams', name: 'Teams Agent' };
  if (text.includes('calendar')) return { id: 'calendar', name: 'Calendar Agent' };
  if (text.includes('summar')) return { id: 'summarize', name: 'Summarize Agent' };
  if (text.includes('q&a') || text.includes('qa')) return { id: 'qa', name: 'Q&A Agent' };
  return { id: 'qa', name: 'Q&A Agent' };
};

const AgentHistory = () => {
  const [sessions, setSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    const fetchHistory = async () => {
      try {
        const res = await axios.get('/core/chat/history/', {
          headers: { Authorization: `Token ${token}` }
        });
        setSessions(res.data);
      } catch (error) {
        console.error('Error fetching agent chat history:', error);
      }
      setIsLoading(false);
    };
    fetchHistory();
  }, [navigate]);

  const handleDeleteChat = async (sessionId) => {
    const result = await Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!',
        background: '#222831',
        color: '#EEEEEE',
    });

    if (result.isConfirmed) {
        try {
            await axios.delete(`/core/chat/session/${sessionId}/delete/`, {
                headers: { Authorization: `Token ${localStorage.getItem('token')}` }
            });
            Swal.fire({
                icon: 'success',
                title: 'Deleted!',
                text: 'Your chat session has been deleted.',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#00ADB5',
            });
            setSessions(sessions.filter(session => session.id !== sessionId));
        } catch (error) {
            console.error('Error deleting chat session:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error!',
                text: 'Could not delete chat session.',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#00ADB5',
            });
        }
    }
  };

  const openSession = (session) => {
    const agent = inferAgentFromSession(session);
    navigate('/agent', { state: { agentId: agent.id, sessionId: session.id } });
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-background via-surface to-primary/10 text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center p-4 w-full">
        <div className="w-full max-w-3xl mx-auto">
          <div className="flex flex-col items-center mb-10 animate-fadeIn">
            <FaHistory className="text-primary text-5xl mb-2 drop-shadow-lg animate-pulse" />
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight text-center">Agent Chat History</h1>
            <p className="text-lg text-accent/80 text-center max-w-xl">Revisit your past agent conversations. Click any session to open it in the Agent workspace.</p>
          </div>
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-16 animate-fadeIn">
              <div className="loader mb-4"></div>
              <p className="text-accent/60 text-lg">Loading agent chat history...</p>
            </div>
          ) : sessions.length > 0 ? (
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-fadeIn">
              {sessions.map((session, idx) => {
                const agent = inferAgentFromSession(session);
                return (
                  <li key={session.id} className="chat-history-card group">
                    <div className="relative block h-full w-full">
                      <div onClick={() => openSession(session)} className="cursor-pointer">
                        <div className="flex flex-col h-full p-6 rounded-2xl shadow-xl bg-surface/80 border border-primary/20 group-hover:scale-[1.03] group-hover:shadow-primary/40 transition-all duration-300 ease-in-out relative overflow-hidden">
                          <div className="flex items-center gap-3 mb-1">
                            <FaComments className="text-primary text-2xl animate-fadeIn" />
                            <span className="font-semibold text-lg text-primary">Session {sessions.length - idx}</span>
                          </div>
                          <div className="text-xs text-accent/70 mb-2">Agent: {agent.name}</div>
                          <p className="text-accent/90 mb-2 truncate">Started: {new Date(session.created_at).toLocaleString()}</p>
                          <span className="text-xs text-accent/60">{session.messages.length} message{session.messages.length !== 1 ? 's' : ''}</span>
                          <div className="absolute right-4 bottom-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-primary text-xl animate-fadeIn">→</div>
                        </div>
                      </div>
                      <button
                          onClick={(e) => {
                              e.preventDefault();
                              e.stopPropagation();
                              handleDeleteChat(session.id);
                          }}
                          className="absolute top-3 right-3 text-red-400 hover:text-red-500 text-xl opacity-0 group-hover:opacity-100 transition-all duration-300 p-1 rounded-full bg-surface/70 hover:bg-surface/90 z-10 transform group-hover:scale-110 active:scale-95"
                          aria-label="Delete chat session"
                      >
                          <FaTimesCircle />
                      </button>
                    </div>
                  </li>
                );
              })}
            </ul>
          ) : (
            <div className="flex flex-col items-center justify-center py-20 animate-fadeIn">
              <FaComments className="text-primary text-6xl mb-6 opacity-80 animate-fadeIn drop-shadow-lg" />
              <p className="text-accent/60 text-xl mb-2">No agent chat history found.</p>
              <button onClick={() => navigate('/agent')} className="mt-4 px-8 py-3 rounded-lg bg-primary text-background font-bold text-lg shadow-lg hover:bg-primary-hover transition-transform hover:scale-105">Open Agent Workspace</button>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default AgentHistory; 