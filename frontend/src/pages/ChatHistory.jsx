import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from '../api/axios';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaHistory, FaComments } from 'react-icons/fa';

const ChatHistory = () => {
    const [sessions, setSessions] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await axios.get('/core/chat/history/', {
                    headers: { Authorization: `Token ${localStorage.getItem('token')}` }
                });
                setSessions(res.data);
            } catch (error) {
                console.error('Error fetching chat history:', error);
            }
            setIsLoading(false);
        };
        fetchHistory();
    }, []);

    return (
        <div className="flex flex-col min-h-screen bg-gradient-to-br from-background via-surface to-primary/10 text-accent font-body">
            <Header />
            <main className="flex-1 flex flex-col items-center justify-center p-4 w-full">
                <div className="w-full max-w-3xl mx-auto">
                  <div className="flex flex-col items-center mb-10 animate-fadeIn">
                    <FaHistory className="text-primary text-5xl mb-2 drop-shadow-lg animate-pulse" />
                    <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight text-center">Chat History</h1>
                    <p className="text-lg text-accent/80 text-center max-w-xl">Easily revisit and continue your past conversations. Click any session to view the full chat.</p>
                  </div>
                  {isLoading ? (
                    <div className="flex flex-col items-center justify-center py-16 animate-fadeIn">
                      <div className="loader mb-4"></div>
                      <p className="text-accent/60 text-lg">Loading chat history...</p>
                    </div>
                  ) : sessions.length > 0 ? (
                    <ul className="grid grid-cols-1 md:grid-cols-2 gap-8 animate-fadeIn">
                      {sessions.map((session, idx) => (
                        <li key={session.id} className="chat-history-card group">
                          <Link to={`/chat/${session.id}`} className="block h-full w-full">
                            <div className="flex flex-col h-full p-6 rounded-2xl shadow-xl bg-surface/80 border border-primary/20 group-hover:scale-[1.03] group-hover:shadow-primary/40 transition-all duration-300 ease-in-out cursor-pointer relative overflow-hidden">
                              <div className="flex items-center gap-3 mb-2">
                                <FaComments className="text-primary text-2xl animate-fadeIn" />
                                <span className="font-semibold text-lg text-primary">Session {sessions.length - idx}</span>
                              </div>
                              <p className="text-accent/90 mb-2 truncate">Started: {new Date(session.created_at).toLocaleString()}</p>
                              <span className="text-xs text-accent/60">{session.messages.length} message{session.messages.length !== 1 ? 's' : ''}</span>
                              <div className="absolute right-4 bottom-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-primary text-xl animate-fadeIn">→</div>
                            </div>
                          </Link>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <div className="flex flex-col items-center justify-center py-20 animate-fadeIn">
                      <FaComments className="text-primary text-6xl mb-6 opacity-80 animate-fadeIn drop-shadow-lg" />
                      <p className="text-accent/60 text-xl mb-2">No chat history found.</p>
                      <Link to="/chat">
                        <button className="mt-4 px-8 py-3 rounded-lg bg-primary text-background font-bold text-lg shadow-lg hover:bg-primary-hover transition-transform hover:scale-105">Start a New Chat</button>
                      </Link>
                    </div>
                  )}
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default ChatHistory;
