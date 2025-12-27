import React, { useState, useEffect, useRef, useLayoutEffect } from 'react';
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

    const messagesContainerRef = useRef(null);
    const isInitialRender = useRef(true);

    const scrollToBottom = () => {
        if (!messagesContainerRef.current) return;
        messagesContainerRef.current.scrollTop =
            messagesContainerRef.current.scrollHeight;
    };

    useEffect(() => {
        const fetchSession = async () => {
            try {
                const res = await axios.get(`/core/chat/session/${sessionId}/`, {
                    headers: {
                        Authorization: `Token ${localStorage.getItem('token')}`,
                    },
                });
                const parsedMessages = res.data.map((msg) => {
                    if (msg.sender === 'agent' && typeof msg.text === 'string') {
                        try {
                            const parsedText = JSON.parse(msg.text);
                            if (typeof parsedText === 'object' && parsedText.result) {
                                return { ...msg, text: parsedText.result };
                            }
                        } catch (e) {
                            // Not a valid JSON string, leave as is
                        }
                    }
                    // Also handle cases where the text might already be an object
                    if (msg.sender === 'agent' && typeof msg.text === 'object' && msg.text.result) {
                        return { ...msg, text: msg.text.result };
                    }
                    return msg;
                });
                setMessages(parsedMessages);
            } catch (error) {
                console.error('Error fetching chat session:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchSession();
    }, [sessionId]);

    useLayoutEffect(() => {
        if (isInitialRender.current) {
            isInitialRender.current = false;
            return;
        }

        if (messages.length <= 1) return;

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
            const res = await axios.post('/agent/respond/', {
                prompt,
                session_id: sessionId,
            });

            setMessages([
                ...newMessages,
                { text: res.data.response.result, sender: 'agent' },
            ]);
        } catch (error) {
            console.error('Error sending message:', error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col min-h-screen bg-gradient-to-b from-background to-surface text-accent font-body">
            <Header />

            <main className="flex-1 flex flex-col items-center p-2 sm:p-4 w-full py-8">
                <div className="w-full max-w-4xl h-[75vh] md:h-[70vh] flex flex-col bg-surface/50 backdrop-blur-sm rounded-2xl shadow-2xl border border-primary/20 overflow-hidden">
                    {/* Messages */}
                    <div
                        ref={messagesContainerRef}
                        className="flex-1 p-4 md:p-6 overflow-y-auto space-y-4"
                    >
                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`flex items-end gap-2 ${
                                    msg.sender === 'user'
                                        ? 'justify-end'
                                        : 'justify-start'
                                }`}
                            >
                                <div
                                    className={`max-w-[85%] md:max-w-lg px-4 py-3 rounded-2xl shadow-md ${
                                        msg.sender === 'user'
                                            ? 'bg-primary/80 text-white rounded-br-none'
                                            : 'bg-surface text-accent rounded-bl-none'
                                    }`}
                                >
                                    <p className="text-sm md:text-base">
                                        {msg.text}
                                    </p>
                                </div>
                            </div>
                        ))}

                        {isLoading && (
                            <div className="flex items-end gap-3 justify-start">
                                <div className="max-w-lg px-4 py-3 rounded-2xl shadow-md bg-surface text-accent rounded-bl-none">
                                    <div className="flex items-center justify-center gap-2">
                                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse" />
                                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse [animation-delay:0.2s]" />
                                        <div className="w-2 h-2 bg-primary rounded-full animate-pulse [animation-delay:0.4s]" />
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Input */}
                    <div className="p-2 sm:p-4 border-t border-primary/20">
                        <form
                            onSubmit={handleSubmit}
                            className="flex items-center gap-2 sm:gap-4"
                        >
                            <input
                                type="text"
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                placeholder="Ask me anything..."
                                className="flex-1 bg-background/50 border-2 border-primary/30 rounded-full py-2 px-4 sm:py-3 sm:px-6 text-accent placeholder-accent/50 focus:outline-none focus:ring-2 focus:ring-primary/50"
                                disabled={isLoading}
                            />
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="bg-primary text-white rounded-full p-3 sm:p-4 shadow-lg hover:bg-primary-hover transition-all disabled:bg-gray-500"
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

export default ChatSession;
