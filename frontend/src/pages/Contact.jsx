import React from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaEnvelope, FaGithub, FaPhoneAlt } from 'react-icons/fa';

export default function Contact() {
  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12 md:py-24 w-full">
        <div className="flex flex-col items-center gap-6 max-w-xl w-full bg-white/90 rounded-xl shadow-xl p-8 animate-fadeIn">
          <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-2 tracking-tight text-center">
            Contact Us
          </h1>
          <p className="text-lg text-accent/80 text-center mb-4">
            Reach out for support, partnership, or feedback. We’d love to hear from you!
          </p>
          <div className="flex flex-col gap-4 w-full">
            <div className="flex items-center gap-3 text-lg group">
              <FaEnvelope className="text-gold group-hover:scale-110 transition-transform duration-200" />
              <a href="mailto:contact@aiagent.com" className="underline hover:text-gold active:text-primary transition group-hover:font-bold">contact@aiagent.com</a>
            </div>
            <div className="flex items-center gap-3 text-lg group">
              <FaGithub className="text-gold group-hover:rotate-12 transition-transform duration-200" />
              <a href="https://github.com/Ghosts6/Local-website" target="_blank" rel="noopener noreferrer" className="underline hover:text-gold active:text-primary transition group-hover:font-bold">AIAgent GitHub</a>
            </div>
            <div className="flex items-center gap-3 text-lg group">
              <FaPhoneAlt className="text-gold group-hover:scale-110 transition-transform duration-200" />
              <span className="group-hover:text-gold transition-colors">+1 (555) 123-4567</span>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
