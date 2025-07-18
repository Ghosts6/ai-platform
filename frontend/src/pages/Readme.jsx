import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ScrollToTopButton from '../components/ScrollToTopButton';
import { FaCrown } from 'react-icons/fa';
import useCodeHighlight from '../hooks/useCodeHighlight';
import 'highlight.js/styles/github-dark.css';
import { marked } from 'marked';

export default function ReadmePage() {
  const [readme, setReadme] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isVisible, setIsVisible] = useState(false);
  useCodeHighlight();

  useEffect(() => {
    fetch('/README.md')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch README.md');
        return res.text();
      })
      .then((text) => {
        setReadme(text);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };
    window.addEventListener('scroll', toggleVisibility);
    return () => window.removeEventListener('scroll', toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center px-4 py-12 md:py-20 w-full">
        <div className="flex flex-col items-center gap-4 w-full bg-surface rounded-xl shadow-xl p-8 relative overflow-hidden">
          <div className="overflow-hidden">
            <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-4 tracking-tight text-center flex items-center gap-2 animate-typing overflow-hidden whitespace-nowrap">
              <FaCrown className="text-primary drop-shadow" /> README
            </h1>
          </div>
          <article className="prose prose-lg max-w-none w-full bg-[#23272f] text-[#f3f6fa] rounded-lg p-4 shadow-inner backdrop-blur-md code-enhanced prose-headings:text-primary prose-a:text-primary prose-pre:bg-[#181b20] prose-code:text-[#00adb5]">
            {loading && <div className="text-center text-accent/60">Loading README...</div>}
            {error && <div className="text-center text-red-600">{error}</div>}
            {!loading && !error && <MarkdownRenderer>{readme}</MarkdownRenderer>}
          </article>
        </div>
      </main>
      <Footer />
      <ScrollToTopButton visible={isVisible} onClick={scrollToTop} />
    </div>
  );
}

function MarkdownRenderer({ children }) {
  return (
    <div
      className="markdown-body"
      dangerouslySetInnerHTML={{ __html: marked.parse(children || '') }}
    />
  );
}
