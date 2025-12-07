import React from 'react';
import { FaArrowUp } from 'react-icons/fa';

export default function ScrollToTopButton({ visible, onClick }) {
  if (!visible) return null;
  return (
    <button 
      onClick={onClick}
      className="fixed bottom-6 right-6 md:bottom-8 md:right-8 bg-primary text-white p-3 md:p-4 rounded-full shadow-xl hover:shadow-2xl hover:bg-primary-hover transition-all duration-300 ease-in-out transform hover:scale-110 active:scale-95 z-50 group"
      aria-label="Scroll to top"
    >
      <FaArrowUp className="h-5 w-5 md:h-6 md:w-6 group-hover:-translate-y-1 transition-transform duration-300" />
    </button>
  );
} 