import React, { useState } from 'react';
import axios from '../api/axios';
import Swal from 'sweetalert2';
import Header from '../components/Header';
import Footer from '../components/Footer';

const Chat = () => {
    const [prompt, setPrompt] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!prompt.trim()) return;

        const newMessages = [...messages, { text: prompt, sender: 'user' }];
        setMessages(newMessages);
        setPrompt('');
        setIsLoading(true);

        try {
            const res = await axios.post('/agent/respond/', { prompt });
            setMessages([...newMessages, { text: res.data.response, sender: 'agent' }]);
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Error communicating with the agent.',
            });
        }
        setIsLoading(false);
    };

    return (
        <div className="flex flex-col min-h-screen bg-background text-accent font-body">
            <Header />
            <main className="flex-1 flex items-center justify-center px-4 py-12 md:py-24 w-full">
                <div className="chat-box">
                    <div className="chat-messages">
                        {messages.map((msg, index) => (
                            <div key={index} className={`message ${msg.sender}`}>
                                {msg.text}
                            </div>
                        ))}
                        {isLoading && <div className="message agent">Thinking...</div>}
                    </div>
                    <form onSubmit={handleSubmit} className="chat-input-form">
                        <input
                            type="text"
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            placeholder="Type your message..."
                            className="chat-input"
                        />
                        <button type="submit" className="chat-send-button" disabled={isLoading}>
                            Send
                        </button>
                    </form>
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default Chat;