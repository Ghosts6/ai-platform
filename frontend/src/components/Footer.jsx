import React from 'react';
import { FaEnvelope, FaGithub, FaLinkedin, FaTwitter } from 'react-icons/fa';

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
    { href: 'https://github.com/Ghosts6/ai-platform', icon: FaGithub, label: 'GitHub', color: 'hover:text-gray-300' },
    { href: 'mailto:kiarash@kiarashbashokian.com', icon: FaEnvelope, label: 'Email', color: 'hover:text-primary' },
  ];

  return (
    <footer className="w-full bg-gradient-to-b from-secondary to-secondary/95 text-accent mt-auto border-t border-primary/20 relative overflow-x-hidden md:overflow-visible">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-primary rounded-full blur-3xl"></div>
      </div>

      <div className="container mx-auto px-4 md:px-6 lg:px-8 py-12 relative z-10">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* Brand Section */}
          <div className="flex flex-col lg:col-span-2">
            <div className="flex items-center gap-3 mb-4 group">
              <div className="relative">
                <div className="absolute inset-0 bg-primary/30 rounded-full blur-md group-hover:blur-lg transition-all duration-300"></div>
                <img 
                  src="/img/logo.png" 
                  alt="AIAgent Logo" 
                  className="h-12 w-12 relative z-10 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-6" 
                />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-primary">AIAgent</h3>
                <span className="text-xs text-accent/60">Smart AI Solutions</span>
              </div>
            </div>
            <p className="text-accent/70 text-sm leading-relaxed mb-6 max-w-md">
              Unlock the full potential of Large Language Models. Seamlessly integrate, manage, and collaborate with digital agents designed for the future of productivity.
            </p>

            {/* Social Links */}
            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <a
                  key={social.label}
                  href={social.href}
                  target={social.href.startsWith('http') ? '_blank' : undefined}
                  rel={social.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                  className={`flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10 text-accent/70 ${social.color} border border-primary/20 hover:border-primary/40 transition-all duration-300 hover:scale-110 active:scale-95 hover:shadow-lg hover:shadow-primary/20`}
                  aria-label={social.label}
                >
                  <social.icon size={20} />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links Section */}
          <div className="flex flex-col">
            <h4 className="text-lg font-bold text-primary mb-4 flex items-center gap-2">
              <span className="w-1 h-6 bg-primary rounded-full"></span>
              Quick Links
            </h4>
            <ul className="space-y-3">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <a
                    href={link.href}
                    className="text-accent/70 hover:text-primary transition-all duration-300 text-sm flex items-center group"
                  >
                    <span className="w-0 group-hover:w-2 h-0.5 bg-primary mr-0 group-hover:mr-2 transition-all duration-300 rounded-full"></span>
                    <span className="group-hover:translate-x-1 transition-transform duration-300">{link.label}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Section */}
          <div className="flex flex-col">
            <h4 className="text-lg font-bold text-primary mb-4 flex items-center gap-2">
              <span className="w-1 h-6 bg-primary rounded-full"></span>
              Get in Touch
            </h4>
            <div className="space-y-4">
              <a
                href="mailto:kiarash@kiarashbashokian.com"
                className="flex items-start gap-3 text-accent/70 hover:text-primary transition-all duration-300 text-sm group p-2 rounded-lg hover:bg-primary/5"
              >
                <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0 group-hover:bg-primary/20 transition-all duration-300">
                  <FaEnvelope className="text-primary w-4 h-4" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-accent/50 mb-1">Email us</span>
                  <span className="break-all font-medium">kiarash@kiarashbashokian.com</span>
                </div>
              </a>
              <a
                href="https://github.com/Ghosts6/ai-platform"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-start gap-3 text-accent/70 hover:text-primary transition-all duration-300 text-sm group p-2 rounded-lg hover:bg-primary/5"
              >
                <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0 group-hover:bg-primary/20 transition-all duration-300">
                  <FaGithub className="text-primary w-4 h-4" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xs text-accent/50 mb-1">Open Source</span>
                  <span className="font-medium">View on GitHub</span>
                </div>
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-primary/20 pt-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex flex-col md:flex-row items-center gap-2 text-sm text-accent/60">
            <div className="flex items-center gap-2">
              <span>&copy; {currentYear}</span>
              <span className="font-semibold text-primary">AIAgent Platform</span>
            </div>
            <span className="hidden md:inline text-accent/40">•</span>
            <span>All rights reserved</span>
          </div>
          <div className="text-sm">
            <span className="font-semibold text-primary">Kiarash B</span>
          </div>
        </div>
      </div>
    </footer>
  );
}