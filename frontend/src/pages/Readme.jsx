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
  const [banner, setBanner] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isVisible, setIsVisible] = useState(false);
  useCodeHighlight();

  useEffect(() => {
    fetch(`/README.md?v=${new Date().getTime()}`)
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch README.md');
        return res.text();
      })
      .then((text) => {
        const bannerRegex = /!\[AIAgent\]\((.*?)\)/;
        const match = text.match(bannerRegex);
        if (match) {
          setBanner(match[1].replace('/frontend/public', '').replace('?raw=true', ''));
          text = text.replace(bannerRegex, '');
        }
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
        <div className="w-full max-w-4xl mx-auto">
          {banner && <img src={banner} alt="AIAgent Banner" className="w-full rounded-t-xl shadow-lg" />}
          <div className="bg-surface rounded-b-xl shadow-xl p-8">
            <article className="prose prose-sm sm:prose-base lg:prose-lg xl:prose-xl max-w-none w-full prose-invert prose-headings:text-primary prose-a:text-primary prose-strong:text-primary prose-blockquote:border-primary prose-code:text-cyan-400 prose-pre:bg-gray-800">
              {loading && <div className="text-center text-accent/60">Loading README...</div>}
              {error && <div className="text-center text-red-600">{error}</div>}
              {!loading && !error && <MarkdownRenderer>{readme}</MarkdownRenderer>}
            </article>
          </div>
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

function rewriteImagePaths(markdown) {
  return markdown.replace(/\]\(\/img\//g, '](/img/');
}
