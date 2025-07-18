import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaEnvelope, FaUser, FaPaperPlane } from 'react-icons/fa';
import Swal from 'sweetalert2';
import axios from '../api/axios';

export default function Contact() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [website, setWebsite] = useState(''); // Honeypot

  const handleSubmit = async (e) => {
    e.preventDefault();

    // If honeypot is filled, do nothing (bot detected)
    if (website) {
      return;
    }

    if (!name || !email || !message) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Please fill out all fields!',
        background: '#393E46',
        color: '#EEEEEE'
      });
      return;
    }

    if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Email',
            text: 'Please enter a valid email address.',
            background: '#393E46',
            color: '#EEEEEE'
        });
        return;
    }

    try {
      // Always send the honeypot field to backend for validation
      const payload = { name, email, message, website };
      const response = await axios.post('/core/contact/', payload);

      Swal.fire({
        icon: 'success',
        title: 'Success!',
        text: response.data.message,
        background: '#393E46',
        color: '#EEEEEE'
      });

      setName('');
      setEmail('');
      setMessage('');
    } catch (error) {
      let errorMessage = 'Something went wrong!';
      if (error.response && error.response.data) {
        if (typeof error.response.data === 'object') {
        errorMessage = Object.values(error.response.data).join(' ');
        } else if (typeof error.response.data === 'string' && error.response.data.startsWith('<')) {
          errorMessage = 'Server error. Please try again later.';
        } else {
          errorMessage = error.response.data;
        }
      }
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: errorMessage,
        background: '#393E46',
        color: '#EEEEEE'
      });
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="w-full max-w-4xl mx-auto bg-surface rounded-2xl shadow-2xl p-8 animate-fadeIn">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight">
              Get in Touch
            </h1>
            <p className="text-lg text-accent/80">
              Have a question or want to work together? Drop a message below.
            </p>
          </div>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="flex flex-col gap-4">
              <div className="relative">
                <FaUser className="absolute top-1/2 -translate-y-1/2 left-4 text-primary" />
                <input type="text" placeholder="Your Name" value={name} onChange={(e) => setName(e.target.value)} className="w-full bg-background border-2 border-secondary rounded-lg p-3 pl-12 focus:outline-none focus:ring-2 focus:ring-primary transition-all" />
              </div>
              <div className="relative">
                <FaEnvelope className="absolute top-1/2 -translate-y-1/2 left-4 text-primary" />
                <input type="email" placeholder="Your Email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full bg-background border-2 border-secondary rounded-lg p-3 pl-12 focus:outline-none focus:ring-2 focus:ring-primary transition-all" />
              </div>
              <input type="text" name="website" value={website} onChange={(e) => setWebsite(e.target.value)} className="hidden" />
            </div>
            <div className="flex flex-col gap-4">
              <textarea placeholder="Your Message" rows="5" value={message} onChange={(e) => setMessage(e.target.value)} className="w-full bg-background border-2 border-secondary rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary transition-all"></textarea>
              <button type="submit" className="w-full bg-primary text-background font-bold py-3 rounded-lg hover:bg-primary-hover transition-colors flex items-center justify-center gap-2">
                <FaPaperPlane /> Send Message
              </button>
            </div>
          </form>
        </div>
      </main>
      <Footer />
    </div>
  );
}