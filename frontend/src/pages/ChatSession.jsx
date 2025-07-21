import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import axios from '../api/axios';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FiSend } from 'react-icons/fi';

const ChatSession = () => {
    const { sessionId } = useParams();
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [prompt, setPrompt] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        const fetchSession = async () => {
            try {
                const res = await axios.get(`/core/chat/session/${sessionId}/`, {
                    headers: { Authorization: `Token ${localStorage.getItem('token')}` }
                });
                setMessages(res.data);
            } catch (error) {
                console.error('Error fetching chat session:', error);
            }
            setIsLoading(false);
        };
        fetchSession();
    }, [sessionId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!prompt.trim()) return;

        const newMessages = [...messages, { text: prompt, sender: 'user' }];
        setMessages(newMessages);
        setPrompt('');
        setIsLoading(true);

        try {
            const res = await axios.post('/agent/respond/', { prompt, session_id: sessionId });
            setMessages([...newMessages, { text: res.data.response, sender: 'agent' }]);
        } catch (error) {
            console.error('Error sending message:', error);
        }
        setIsLoading(false);
    };

    return (
        <div className="flex flex-col min-h-screen bg-gradient-to-b from-background to-surface text-accent font-body">
            <Header />
            <main className="flex-1 flex items-center justify-center p-4 w-full">
                <div className="w-full max-w-4xl h-[75vh] flex flex-col bg-surface/50 backdrop-blur-sm rounded-2xl shadow-2xl border border-primary/20 overflow-hidden">
                    <div className="flex-1 p-6 overflow-y-auto space-y-4">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex items-end gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-lg px-4 py-3 rounded-2xl shadow-md transition-all duration-300 ${
                                    msg.sender === 'user' 
                                        ? 'bg-primary/80 text-white rounded-br-none' 
                                        : 'bg-surface text-accent rounded-bl-none'
                                }`}>
                                    <p className="text-sm md:text-base">{msg.text}</p>
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex items-end gap-3 justify-start">
                                <div className="max-w-lg px-4 py-3 rounded-2xl shadow-md bg-surface text-accent rounded-bl-none">
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
                    <div className="p-4 border-t border-primary/20">
                        <form onSubmit={handleSubmit} className="flex items-center gap-4">
                            <input
                                type="text"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                placeholder="Ask me anything..."
                                className="flex-1 bg-background/50 border-2 border-primary/30 rounded-full py-3 px-6 text-accent placeholder-accent/50 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300"
                                disabled={isLoading}
                            />
                            <button 
                                type="submit" 
                                className="bg-primary text-white rounded-full p-4 shadow-lg hover:bg-primary-hover transform hover:scale-110 transition-all duration-300 disabled:bg-gray-500 disabled:scale-100" 
                                disabled={isLoading}
                            >
                                <FiSend className="w-6 h-6" />
                            </button>
                        </form>
                    </div>
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default ChatSession;
