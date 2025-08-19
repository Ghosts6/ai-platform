
import React, { useState, useRef, useEffect } from 'react';
import axios from '../api/axios';
import Swal from 'sweetalert2';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FiSend } from 'react-icons/fi';

const Chat = () => {
    const [prompt, setPrompt] = useState('');
    const [messages, setMessages] = useState([{
        text: "Hi! I'm your AI assistant. How can I help you today? You can ask me anything you need!",
        sender: 'agent'
    }]);
    const [isLoading, setIsLoading] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
    const messagesEndRef = useRef(null);

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
                confirmButtonColor: '#007bff',
            });
        }
    }, [isLoggedIn]);

    const [session_id, setSessionId] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!prompt.trim()) return;

        const newMessages = [...messages, { text: prompt, sender: 'user' }];
        setMessages(newMessages);
        setPrompt('');
        setIsLoading(true);

        try {
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

    return (
        <div className="flex flex-col min-h-screen bg-gradient-to-b from-background to-surface text-accent font-body">
            <Header />
            <main className="flex-1 flex flex-col items-center justify-center p-2 sm:p-4 w-full">
                <div className="w-full max-w-4xl h-[85vh] sm:h-[75vh] flex flex-col bg-surface/50 backdrop-blur-sm rounded-2xl shadow-2xl border border-primary/20 overflow-hidden">
                    <div className="flex-1 p-4 md:p-6 overflow-y-auto space-y-4">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex items-end gap-2 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-md md:max-w-lg px-4 py-2 md:py-3 rounded-2xl shadow-md transition-all duration-300 ${
                                    msg.sender === 'user' 
                                        ? 'bg-primary/80 text-white rounded-br-none' 
                                        : 'bg-surface text-accent rounded-bl-none'
                                }`}>
                                    <p className="text-sm md:text-base">{msg.text}</p>
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex items-end gap-2 justify-start">
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
                    <div className="p-2 sm:p-4 border-t border-primary/20">
                        <form onSubmit={handleSubmit} className="flex items-center gap-2 sm:gap-4">
                            <input
                                type="text"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                placeholder="Ask me anything..."
                                className="flex-1 bg-background/50 border-2 border-primary/30 rounded-full py-2 px-4 sm:py-3 sm:px-6 text-sm sm:text-base text-accent placeholder-accent/50 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300"
                                disabled={isLoading}
                            />
                            <button 
                                type="submit" 
                                className="bg-primary text-white rounded-full p-3 sm:p-4 shadow-lg hover:bg-primary-hover transform hover:scale-110 transition-all duration-300 disabled:bg-gray-500 disabled:scale-100" 
                                disabled={isLoading}
                            >
                                <FiSend className="w-5 h-5 sm:w-6 sm:h-6" />
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
