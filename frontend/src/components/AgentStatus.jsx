import React from 'react';
import { FiZap, FiCheckCircle, FiAlertCircle, FiClock, FiXCircle } from 'react-icons/fi';

const AgentStatus = ({ agent, isSelected, onClick }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <FiCheckCircle className="w-4 h-4 text-green-500" />;
      case 'inactive':
        return <FiXCircle className="w-4 h-4 text-gray-500" />;
      case 'error':
        return <FiAlertCircle className="w-4 h-4 text-red-500" />;
      case 'processing':
        return <FiClock className="w-4 h-4 text-yellow-500" />;
      default:
        return <FiXCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-500';
      case 'inactive': return 'text-gray-500';
      case 'error': return 'text-red-500';
      case 'processing': return 'text-yellow-500';
      default: return 'text-gray-500';
    }
  };

  const getStatusBg = (status) => {
    switch (status) {
      case 'active': return 'bg-green-500/20';
      case 'inactive': return 'bg-gray-500/20';
      case 'error': return 'bg-red-500/20';
      case 'processing': return 'bg-yellow-500/20';
      default: return 'bg-gray-500/20';
    }
  };

  return (
    <div
      className={`p-4 rounded-lg border-2 transition-all duration-300 cursor-pointer hover:shadow-lg ${
        isSelected 
          ? 'border-primary bg-primary/10 shadow-primary/20' 
          : 'border-transparent hover:border-primary/30 bg-surface/50 hover:bg-surface/70'
      }`}
      onClick={() => onClick(agent)}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary/20 rounded-lg flex items-center justify-center">
            <agent.icon className="w-4 h-4 text-primary" />
          </div>
          <span className="font-semibold text-accent">{agent.name}</span>
        </div>
        <div className="flex items-center gap-2">
          {getStatusIcon(agent.status)}
          <span className={`text-xs px-2 py-1 rounded-full ${getStatusBg(agent.status)} ${getStatusColor(agent.status)}`}>
            {agent.status}
          </span>
        </div>
      </div>
      
      <p className="text-sm text-accent/70 mb-3 line-clamp-2">{agent.description}</p>
      
      <div className="space-y-2">
        <div className="flex items-center gap-2">
          <FiZap className="w-3 h-3 text-primary" />
          <span className="text-xs text-accent/60 font-medium">Capabilities:</span>
        </div>
        <div className="flex flex-wrap gap-1">
          {agent.capabilities.slice(0, 2).map((capability, index) => (
            <span
              key={index}
              className="text-xs px-2 py-1 bg-primary/20 text-primary rounded-full"
            >
              {capability}
            </span>
          ))}
          {agent.capabilities.length > 2 && (
            <span className="text-xs px-2 py-1 bg-secondary/30 text-accent/60 rounded-full">
              +{agent.capabilities.length - 2}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentStatus; 