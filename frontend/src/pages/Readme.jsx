import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { FaBookOpen, FaCrown } from 'react-icons/fa';
import useCodeHighlight from '../hooks/useCodeHighlight';
import 'highlight.js/styles/github-dark.css';
import { marked } from 'marked';

export default function ReadmePage() {
  const [readme, setReadme] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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

  return (
    <div className="flex flex-col min-h-screen bg-background text-accent font-body">
      <Header />
      <main className="flex-1 flex flex-col items-center px-4 py-12 md:py-20 w-full">
        <div className="flex flex-col items-center gap-4 max-w-3xl w-full bg-white/90 rounded-xl shadow-xl p-8 relative overflow-hidden">
          <FaBookOpen className="absolute top-4 right-4 text-gold text-4xl opacity-30 pointer-events-none" />
          <h1 className="text-4xl md:text-5xl font-display font-extrabold text-primary mb-4 tracking-tight text-center flex items-center gap-2">
            <FaCrown className="text-gold drop-shadow" /> README
          </h1>
          <article className="prose prose-lg max-w-none w-full text-black/90 bg-white/80 rounded-lg p-4 shadow-inner backdrop-blur-md code-enhanced">
            {loading && <div className="text-center text-accent/60">Loading README...</div>}
            {error && <div className="text-center text-red-600">{error}</div>}
            {!loading && !error && <MarkdownRenderer>{readme}</MarkdownRenderer>}
          </article>
        </div>
      </main>
      <Footer />
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

// Add to tailwind.config.js for prose/code styling if not present:
//   require('@tailwindcss/typography'),
