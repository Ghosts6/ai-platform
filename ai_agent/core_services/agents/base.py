from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentBase(ABC):
    """Enhanced base class for all AI agents with configuration and state management"""
    
    def __init__(self, agent_id: str, name: str, description: str = ""):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.config = {}
        self.memory = {}
        self.status = "idle"
        self.created_at = datetime.now()
        self.last_used = None
        
    @abstractmethod
    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        pass
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Update agent configuration"""
        self.config.update(config)
        logger.info(f"Agent {self.name} configured with: {config}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "capabilities": self.get_capabilities()
        }
    
    def store_memory(self, key: str, value: Any) -> None:
        """Store persistent memory for this agent"""
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    def retrieve_memory(self, key: str, default: Any = None) -> Any:
        """Retrieve stored memory"""
        memory_data = self.memory.get(key)
        return memory_data["value"] if memory_data else default
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for this agent"""
        required_fields = ["type", "prompt"]
        return all(field in task for field in required_fields)
    
    def format_response(self, result: Any, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format response consistently"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "result": result,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }


    def _update_status(self, new_status: str) -> None:
        """Internal method to update agent status"""
        self.status = new_status
        logger.debug(f"Agent {self.name} status changed to: {new_status}")
        
    def _log_usage(self) -> None:
        """Internal method to log agent usage"""
        self.last_used = datetime.now()
        logger.info(f"Agent {self.name} was used at {self.last_used.isoformat()}")
        
    def to_json(self) -> str:
        """Serialize agent state to JSON"""
        return json.dumps({
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "config": self.config,
            "memory": self.memory,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None
        }, indent=4)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AgentBase':
        """Deserialize agent from JSON"""
        data = json.loads(json_str)
        agent = cls(agent_id=data['agent_id'], name=data['name'], description=data.get('description', ''))
        agent.config = data.get('config', {})
        agent.memory = data.get('memory', {})
        agent.status = data.get('status', 'idle')
        agent.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('last_used'):
            agent.last_used = datetime.fromisoformat(data['last_used'])
        return agent
    
    def __repr__(self) -> str:
        return f"<EnhancedAgent(id={self.agent_id}, name='{self.name}', status='{self.status}')>"
    
    async def handle_task(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """A wrapper method to handle a task with logging, status updates, and validation"""
        self._update_status("processing")
        self._log_usage()
        
        if not self.validate_task(task):
            self._update_status("error")
            return self.format_response(result="Invalid task structure", metadata={"error": "Missing required fields"})
        
        try:
            result = await self.process(task, context)
            self._update_status("idle")
            return self.format_response(result)
        except Exception as e:
            logger.error(f"Error processing task in agent {self.name}: {e}", exc_info=True)
            self._update_status("error")
            return self.format_response(result=str(e), metadata={"error": "An unexpected error occurred"})