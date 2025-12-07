import React from 'react';
import { FaEnvelope, FaGithub, FaLinkedin, FaTwitter, FaHeart } from 'react-icons/fa';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const quickLinks = [
    { href: '/', label: 'Home' },
    { href: '/chatbot', label: 'Chatbot' },
    { href: '/agents', label: 'Agents' },
    { href: '/readme', label: 'README' },
    { href: '/contact', label: 'Contact' },
  ];

  const socialLinks = [
    { href: 'https://github.com/Ghosts6/ai-platform', icon: FaGithub, label: 'GitHub', color: 'hover:text-gray-400' },
    { href: 'mailto:kiarash@kiarashbashokian.com', icon: FaEnvelope, label: 'Email', color: 'hover:text-primary' },
  ];

  return (
    <footer className="w-full bg-secondary text-accent mt-auto border-t border-primary/30">
      <div className="container mx-auto px-4 md:px-6 lg:px-8 py-8">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Brand Section */}
          <div className="flex flex-col">
            <div className="flex items-center mb-4">
              <img src="/img/logo.png" alt="AIAgent Logo" className="h-10 w-10 mr-2" />
              <h3 className="text-2xl font-bold text-primary">AIAgent</h3>
            </div>
            <p className="text-accent/70 text-sm leading-relaxed mb-4">
              Unlock the full potential of Large Language Models. Seamlessly integrate, manage, and collaborate with digital agents designed for the future of productivity.
            </p>
            <div className="flex gap-4">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target={social.href.startsWith('http') ? '_blank' : undefined}
                  rel={social.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                  className={`text-accent/70 ${social.color} transition-all duration-300 transform hover:scale-110 active:scale-95`}
                  aria-label={social.label}
                >
                  <social.icon size={24} />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links Section */}
          <div className="flex flex-col">
            <h4 className="text-lg font-bold text-primary mb-4">Quick Links</h4>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className="text-accent/70 hover:text-primary transition-colors duration-300 text-sm flex items-center group"
                  >
                    <span className="w-0 group-hover:w-2 h-0.5 bg-primary mr-0 group-hover:mr-2 transition-all duration-300"></span>
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Section */}
          <div className="flex flex-col">
            <h4 className="text-lg font-bold text-primary mb-4">Get in Touch</h4>
            <div className="space-y-3">
              <a
                href="mailto:kiarash@kiarashbashokian.com"
                className="flex items-center gap-2 text-accent/70 hover:text-primary transition-colors duration-300 text-sm group"
              >
                <FaEnvelope className="text-primary group-hover:scale-110 transition-transform duration-300" />
                <span className="break-all">kiarash@kiarashbashokian.com</span>
              </a>
              <a
                href="https://github.com/Ghosts6/ai-platform"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 text-accent/70 hover:text-primary transition-colors duration-300 text-sm group"
              >
                <FaGithub className="text-primary group-hover:scale-110 transition-transform duration-300" />
                <span>View on GitHub</span>
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-primary/20 pt-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-sm text-accent/60">
            <span>&copy; {currentYear}</span>
            <span>AIAgent Platform</span>
            <span className="hidden md:inline">•</span>
            <span className="hidden md:inline">All rights reserved</span>
          </div>
          <div className="flex items-center gap-1 text-sm text-accent/60">
            <span>kiarash b</span>
          </div>
        </div>
      </div>
    </footer>
  );
}