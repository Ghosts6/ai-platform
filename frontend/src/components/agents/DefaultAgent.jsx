import React from 'react';
import { FiPlay } from 'react-icons/fi';

const DefaultAgent = ({ selectedAgent, prompt, setPrompt, response, isLoading, handleSubmit }) => {
  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-4">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder={`What should I ask the ${selectedAgent.name}?`}
          className="w-full bg-surface/50 text-accent border-2 border-primary/30 rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300 h-40 resize-none"
        />
      </div>
      <button
        type="submit"
        disabled={isLoading || !prompt.trim()}
        className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-hover transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-primary/25 transform hover:scale-105"
      >
        {isLoading ? (
          <>
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            Processing...
          </>
        ) : (
          <>
            <FiPlay className="w-5 h-5" />
            Submit to Agent
          </>
        )}
      </button>

      {response && (
        <div className="mt-8 p-6 bg-surface/50 rounded-xl border border-primary/20 animate-fade-in">
          <h3 className="text-2xl font-bold text-primary mb-4">Agent Response</h3>
          <div className="bg-background/50 p-4 rounded-lg">
            <pre className="whitespace-pre-wrap text-accent/80 font-mono text-sm">{response}</pre>
          </div>
        </div>
      )}
    </form>
  );
};

export default DefaultAgent;
