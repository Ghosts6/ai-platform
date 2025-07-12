import 'highlight.js/styles/github-dark.css';
import hljs from 'highlight.js';
import { useEffect } from 'react';

export default function useCodeHighlight() {
  useEffect(() => {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightElement(block);
    });
  }, []);
}
