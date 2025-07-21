import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaRobot, FaComments, FaHistory, FaListAlt } from 'react-icons/fa';
import axios from '../api/axios';
import Swal from 'sweetalert2';

export default function Agent() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const navigate = useNavigate();

  useEffect(() => {
    const handleStorage = () => setIsLoggedIn(!!localStorage.getItem('token'));
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  const handleHistoryClick = () => {
    if (isLoggedIn) {
      navigate('/chat/history');
    } else {
      navigate('/login');
    }
  };

  const handleContinueChat = async () => {
    if (!isLoggedIn) {
      navigate('/login');
      return;
    }
    try {
      const res = await axios.get('/core/chat/last/', {
        headers: { Authorization: `Token ${localStorage.getItem('token')}` }
      });
      if (res.data && res.data.id) {
        navigate(`/chat/${res.data.id}`);
      } else {
        Swal.fire({
          icon: 'info',
          title: 'No Previous Chat',
          text: 'You have no previous chat sessions. Start a new chat!',
          background: '#222831',
          color: '#EEEEEE',
          confirmButtonColor: '#007bff',
        });
      }
    } catch (error) {
      Swal.fire({
        icon: 'info',
        title: 'No Previous Chat',
        text: 'You have no previous chat sessions. Start a new chat!',
        background: '#222831',
        color: '#EEEEEE',
        confirmButtonColor: '#007bff',
      });
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="w-full max-w-4xl mx-auto bg-surface rounded-2xl shadow-2xl p-8 animate-fadeIn">
          <div className="text-center mb-8">
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight flex items-center justify-center gap-3">
              <FaRobot className="text-primary animate-bounce" /> Agent Management
            </h1>
            <p className="text-lg text-accent/80">
              Start a new chat, continue a previous conversation, or view all your past chats.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-background p-6 rounded-lg shadow-lg hover:shadow-primary/50 transition-shadow duration-300">
              <div className="flex items-center gap-4 mb-4">
                <FaComments className="text-primary text-3xl" />
                <h2 className="text-2xl font-bold">Start Chat</h2>
              </div>
              <p className="text-accent/80">Start a new conversation with an AI agent to get assistance.</p>
              <Link to="/chat" className="mt-4 w-full">
                <button className="w-full bg-primary text-white font-bold py-2 px-4 rounded hover:bg-primary/80 transition-colors duration-300">Start New Chat</button>
              </Link>
            </div>
            <div className="bg-background p-6 rounded-lg shadow-lg hover:shadow-primary/50 transition-shadow duration-300">
              <div className="flex items-center gap-4 mb-4">
                <FaHistory className="text-primary text-3xl" />
                <h2 className="text-2xl font-bold">Continue Chat</h2>
              </div>
              <p className="text-accent/80">Resume a previous conversation from your chat history.</p>
              <button onClick={handleContinueChat} className="mt-4 w-full bg-primary text-white font-bold py-2 px-4 rounded hover:bg-primary/80 transition-colors duration-300">Continue</button>
            </div>
            <div className="bg-background p-6 rounded-lg shadow-lg hover:shadow-primary/50 transition-shadow duration-300">
              <div className="flex items-center gap-4 mb-4">
                <FaListAlt className="text-primary text-3xl" />
                <h2 className="text-2xl font-bold">List of Chats</h2>
              </div>
              <p className="text-accent/80">View a complete list of all your past conversations.</p>
              <button onClick={handleHistoryClick} className="mt-4 w-full bg-primary text-white font-bold py-2 px-4 rounded hover:bg-primary/80 transition-colors duration-300">View Chats</button>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}