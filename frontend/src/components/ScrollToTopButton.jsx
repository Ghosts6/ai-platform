import React from 'react';
import { FaArrowUp } from 'react-icons/fa';

export default function ScrollToTopButton({ visible, onClick }) {
  if (!visible) return null;
  return (
    <button 
      onClick={onClick}
      className="fixed bottom-8 right-8 bg-primary text-white p-4 rounded-full shadow-lg hover:bg-primary-hover active:bg-primary-dark transition-all duration-300 ease-in-out transform hover:scale-110 active:scale-100 z-50"
      aria-label="Scroll to top"
    >
      <FaArrowUp className="h-6 w-6" />
    </button>
  );
} 