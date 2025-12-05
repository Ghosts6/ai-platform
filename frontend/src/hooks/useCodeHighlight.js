import 'highlight.js/styles/github-dark.css';
import hljs from 'highlight.js';
import { useEffect } from 'react';

export default function useCodeHighlight() {
  useEffect(() => {
    document.querySelectorAll('pre').forEach((pre) => {
      const code = pre.querySelector('code');
      if (code) {
        hljs.highlightElement(code);
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button-icon';
        copyButton.innerHTML = '<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>';
        pre.appendChild(copyButton);
        copyButton.addEventListener('click', () => {
          navigator.clipboard.writeText(code.textContent);
          copyButton.innerHTML = 'Copied!';
          setTimeout(() => {
            copyButton.innerHTML = '<svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>';
          }, 2000);
        });
      }
    });
  }, []);
}
