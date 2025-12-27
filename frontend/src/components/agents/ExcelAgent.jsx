import React, { useEffect, useRef, useMemo } from 'react';
import FileUpload from '../FileUpload';
import { FiPlay, FiCopy } from 'react-icons/fi';
import Swal from 'sweetalert2';

const ExcelAgent = ({ selectedAgent, prompt, setPrompt, response, isLoading, handleSubmit, selectedFile, setSelectedFile }) => {
  const chatEndRef = useRef(null);

  const excelMessages = useMemo(() => {
    if (!response) return [];
    return response.split('\n\n').map(line => {
      const [sender, ...textParts] = line.split(': ');
      return { sender, text: textParts.join(': ') };
    });
  }, [response]);

  /* useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [excelMessages]); */

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      Swal.fire({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 1200,
        background: '#222831',
        color: '#EEEEEE',
        icon: 'success',
        title: 'Copied',
      });
    } catch {}
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (prompt.trim()) {
        handleSubmit(e);
      }
    }
  };

  return (
    <div>
      <div className="mb-4 p-4 bg-surface/50 rounded-xl border border-primary/20">
        <FileUpload onFileChange={handleFileChange} selectedFile={selectedFile} />
        {selectedFile && (
          <div className="mt-2 text-sm text-accent/70">Selected file: {selectedFile.name}</div>
        )}
      </div>

      <div className="flex flex-col gap-3 max-h-[50vh] overflow-y-auto p-4 bg-background/50 rounded-xl border border-primary/20">
        {excelMessages.length === 0 && !isLoading && (
          <div className="text-accent/60 text-sm">
            Start by uploading a file (CSV, TSV, JSON, XLS/XLSX) and ask things like "describe", "head", "columns", "rows", or "convert to xlsx".
          </div>
        )}
        {excelMessages.map((m, idx) => (
          <div key={idx} className={`max-w-[80%] p-3 rounded-lg ${m.sender === 'user' ? 'self-end bg-primary text-white' : 'self-start bg-surface/70 border border-primary/20'}`}>
            <pre className={`whitespace-pre-wrap font-sans text-sm ${m.sender === 'user' ? 'text-white' : 'text-accent/90'}`}>{m.text}</pre>
            <div className="flex justify-end mt-1">
              <button
                onClick={() => copyToClipboard(m.text)}
                className="text-accent/50 hover:text-accent transition-colors"
                title="Copy"
              >
                <FiCopy className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="self-start max-w-[60%] p-3 rounded-lg bg-surface/70 border border-primary/20 text-accent/70 text-sm">
            Typing...
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="mt-4 flex gap-3">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={`Message ${selectedAgent.name}...`}
          className="flex-1 bg-surface/50 text-accent border-2 border-primary/30 rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent transition-all duration-300 h-24 resize-none"
        />
        <button
          type="submit"
          disabled={isLoading || !prompt.trim()}
          className="bg-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-hover transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg hover:shadow-primary/25"
        >
          <FiPlay className="w-5 h-5" />
          Send
        </button>
      </form>
    </div>
  );
};

export default ExcelAgent;