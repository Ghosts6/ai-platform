import React, { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from '../api/axios';
import Swal from 'sweetalert2';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FiSend, FiArrowLeft, FiCpu, FiUser } from 'react-icons/fi';

const Chat = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [prompt, setPrompt] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
    const [session_id, setSessionId] = useState(null);
    const [agentInfo, setAgentInfo] = useState(null);
    const messagesEndRef = useRef(null);

    // Get agent info from navigation state
    useEffect(() => {
        if (location.state) {
            const { agentId, agentName, initialQuery } = location.state;
            setAgentInfo({ id: agentId, name: agentName });
            
            // Set initial message based on agent
            const initialMessage = agentId === 'general' 
                ? "Hi! I'm your AI Manager. I can help you with various tasks and route your requests to the most appropriate specialized agent. What would you like to do today?"
                : `Hi! I'm your ${agentName}. I'm specialized in ${getAgentSpecialty(agentId)}. How can I assist you today?`;
            
            setMessages([{
                text: initialMessage,
                sender: 'agent'
            }]);

            // If there's an initial query, send it automatically
            if (initialQuery) {
                setPrompt(initialQuery);
                setTimeout(() => handleSubmit(new Event('submit')), 500);
            }
        } else {
            // Default agent if no specific agent selected
            setAgentInfo({ id: 'general', name: 'AI Assistant' });
            setMessages([{
                text: "Hi! I'm your AI assistant. How can I help you today? You can ask me anything you need!",
                sender: 'agent'
            }]);
        }
    }, [location.state]);

    const getAgentSpecialty = (agentId) => {
        const specialties = {
            'email': 'email composition, analysis, and management',
            'excel': 'Excel operations, data analysis, and spreadsheet tasks',
            'qa': 'answering questions and providing information',
            'summarize': 'creating concise summaries and content analysis',
            'teams': 'team collaboration and scheduling',
            'list': 'list management and data organization',
            'calendar': 'calendar and scheduling management',
            'general': 'managing and routing tasks to specialized agents'
        };
        return specialties[agentId] || 'various tasks and workflows';
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        if (!isLoggedIn) {
            Swal.fire({
                icon: 'info',
                title: 'Guest User',
                text: 'Your chat history will not be saved. Please login to save your chats.',
                background: '#222831',
                color: '#EEEEEE',
                confirmButtonColor: '#00ADB5',
            });
        }
    }, [isLoggedIn]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!prompt.trim()) return;

        const newMessages = [...messages, { text: prompt, sender: 'user' }];
        setMessages(newMessages);
        setPrompt('');
        setIsLoading(true);

        try {
            // Use your existing agent API endpoint
            const res = await axios.post('/agent/respond/', { prompt, session_id });
            setMessages([...newMessages, { text: res.data.response, sender: 'agent' }]);
            if (isLoggedIn && !session_id) {
                setSessionId(res.data.session_id);
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Error communicating with the agent.',
                customClass: {
                    popup: 'bg-surface',
                    title: 'text-red-500',
                    content: 'text-accent'
                }
            });
        }
        setIsLoading(false);
    };

    const handleBackToAgents = () => {
        navigate('/agents');
    };

    return (
        <div className="flex flex-col min-h-screen bg-gradient-to-b from-background to-surface text-accent font-body">
            <Header />
            <main className="flex-1 flex flex-col items-center justify-center p-2 sm:p-4 w-full">
                <div className="w-full max-w-5xl h-[85vh] sm:h-[75vh] flex flex-col bg-surface/50 backdrop-blur-sm rounded-2xl shadow-2xl border border-primary/20 overflow-hidden">
                    {/* Chat Header */}
                    <div className="bg-gradient-to-r from-primary/20 to-secondary/20 p-4 border-b border-primary/20">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <button
                                    onClick={handleBackToAgents}
                                    className="p-2 rounded-lg bg-primary/20 text-primary hover:bg-primary/30 transition-colors duration-200"
                                >
                                    <FiArrowLeft className="w-5 h-5" />
                                </button>
                                <div className="flex items-center gap-2">
                                    <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                                        <FiCpu className="w-5 h-5 text-white" />
                                    </div>
                                    <div>
                                        <h2 className="text-lg font-bold text-primary">{agentInfo?.name}</h2>
                                        <p className="text-xs text-accent/70">{getAgentSpecialty(agentInfo?.id)}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Chat Messages */}
                    <div className="flex-1 p-4 md:p-6 overflow-y-auto space-y-4">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex items-end gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                {msg.sender === 'agent' && (
                                    <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                                        <FiCpu className="w-4 h-4 text-white" />
                                    </div>
                                )}
                                
                                <div className={`max-w-md md:max-w-lg px-4 py-2 md:py-3 rounded-2xl shadow-md transition-all duration-300 ${
                                    msg.sender === 'user' 
                                        ? 'bg-primary/80 text-white rounded-br-none' 
                                        : 'bg-surface text-accent rounded-bl-none'
                                }`}>
                                    <p className="text-sm md:text-base">{msg.text}</p>
                                </div>

                                {msg.sender === 'user' && (
                                    <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0">
                                        <FiUser className="w-4 h-4 text-accent" />
                                    </div>
                                )}
                            </div>
                        ))}
                        
                        {isLoading && (
                            <div className="flex items-end gap-3 justify-start">
                                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                                    <FiCpu className="w-4 h-4 text-white" />
                                </div>
                                <div className="max-w-md md:max-w-lg px-4 py-2 md:py-3 rounded-2xl shadow-md bg-surface text-accent rounded-bl-none">
                                    <div className="flex items-center justify-center gap-2">
                                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse [animation-delay:0.2s]"></div>
                                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse [animation-delay:0.4s]"></div>
                                    </div>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Chat Input */}
                    <div className="p-4 border-t border-primary/20 bg-surface/30">
                        <form onSubmit={handleSubmit} className="flex gap-3">
                            <input
                                type="text"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                placeholder={`Ask ${agentInfo?.name} anything...`}
                                className="flex-1 bg-background text-accent border-2 border-primary/30 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300"
                                disabled={isLoading}
                            />
                            <button
                                type="submit"
                                disabled={!prompt.trim() || isLoading}
                                className="bg-primary text-white p-3 rounded-xl font-semibold hover:bg-primary-hover transition-colors duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                            >
                                <FiSend className="w-5 h-5" />
                            </button>
                        </form>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default Chat;