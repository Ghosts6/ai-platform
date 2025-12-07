import React, { useState, useEffect, useRef } from 'react';
import axios from '../../api/axios';
import Swal from 'sweetalert2';
import FileUpload from '../FileUpload';
import { FiPlay } from 'react-icons/fi';

const ExcelAgent = ({ selectedAgent, prompt, setPrompt, response, setResponse, isLoading, setIsLoading, handleSubmit: genericHandleSubmit }) => {
  const [excelMessages, setExcelMessages] = useState([]); // {sender: 'user'|'agent', text: string}
  const [excelSessionId, setExcelSessionId] = useState(null);
  const [excelTyping, setExcelTyping] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current && excelMessages.length > 0) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [excelMessages, excelTyping]);

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
        const fakeEvent = { preventDefault: () => {} };
        handleSubmit(fakeEvent);
      }
    }
  };

  const showError = (error, fallback = 'Error communicating with the agent.') => {
    let msg = fallback;
    if (error?.response?.data?.error) {
      msg = error.response.data.error;
    } else if (typeof error?.message === 'string') {
      msg = error.message;
    }
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: msg,
      background: '#222831',
      color: '#EEEEEE',
      confirmButtonColor: '#00ADB5',
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    const userMsg = { sender: 'user', text: prompt };
    setExcelMessages(prev => [...prev, userMsg]);
    setExcelTyping(true);
    setPrompt('');
    try {
      let res;
      if (selectedFile) {
        const formData = new FormData();
        formData.append('prompt', userMsg.text);
        formData.append('agent', 'excel');
        if (excelSessionId) formData.append('session_id', excelSessionId);
        formData.append('file', selectedFile);
        res = await axios.post('/agent/respond/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      } else {
        const payload = { prompt: userMsg.text, agent: 'excel' };
        if (excelSessionId) payload.session_id = excelSessionId;
        res = await axios.post('/agent/respond/', payload);
      }
      const agentText = res.data.response;
      const newSessionId = res.data.session_id || excelSessionId;
      if (newSessionId && newSessionId !== excelSessionId) setExcelSessionId(newSessionId);
      setExcelMessages(prev => [...prev, { sender: 'agent', text: agentText }]);
    } catch (error) {
      showError(error, 'Error communicating with the Excel agent.');
    }
    setExcelTyping(false);
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
        {excelMessages.length === 0 && (
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
                <FiPlay className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
        {excelTyping && (
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
          disabled={!prompt.trim()}
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