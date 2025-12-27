from ai_agent.core_services.models import Agent, AgentMemory, AgentLog
from asgiref.sync import sync_to_async
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime
from django.utils import timezone
from ai_agent.shared_utils import es_client as es_client_module

logger = logging.getLogger(__name__)

class AgentBase(ABC):
    """Enhanced base class for all AI agents with configuration and state management"""
    
    def __init__(self, agent_instance: Agent):
        self.agent_instance = agent_instance
        self.name = agent_instance.name
        self.description = agent_instance.description
        self.config = agent_instance.configuration if agent_instance.configuration else {}
        self.memory = {} # Will be loaded from DB
        self.status = agent_instance.status
        self.created_at = agent_instance.created_at
        self.last_used = agent_instance.last_used
        
    @abstractmethod
    async def process(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a task and return results"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        pass
    
    def validate_task(self, task: Dict[str, Any]) -> bool:
        """Validate if task is suitable for this agent"""
        required_fields = ["type", "prompt"]
        return all(field in task for field in required_fields)
    
    def format_response(self, result: Any, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Format response consistently"""
        return {
            "agent_id": str(self.agent_instance.id),
            "agent_name": self.name,
            "result": result,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Update agent configuration"""
        self.config.update(config)
        logger.info(f"Agent {self.name} configured with: {config}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent_id": str(self.agent_instance.id),
            "name": self.name,
            "status": self.status,
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "capabilities": self.get_capabilities()
        }
    
    async def _load_memory(self):
        """Asynchronously loads all memory entries for this agent from the database."""
        try:
            memory_entries = await sync_to_async(list)(AgentMemory.objects.filter(agent_name=self.agent_instance.name))
            self.memory = {entry.key: json.loads(entry.value) for entry in memory_entries}
            logger.debug(f"Memory loaded for agent {self.name}")
        except Exception as e:
            logger.error(f"Error loading memory for agent {self.name}: {e}")
            self.memory = {}

    async def _save_memory(self):
        """Asynchronously saves all current memory entries to the database."""
        for key, value_data in self.memory.items():
            try:
                await sync_to_async(AgentMemory.objects.update_or_create)(
                    agent_name=self.agent_instance.name,
                    key=key,
                    defaults={'value': json.dumps(value_data)}
                )
            except Exception as e:
                logger.error(f"Error saving memory key {key} for agent {self.name}: {e}")
        logger.debug(f"Memory saved for agent {self.name}")

    async def store_memory(self, key: str, value: Any) -> None:
        """Store persistent memory for this agent and save to DB."""
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        await self._save_memory()

    async def retrieve_memory(self, key: str, default: Any = None) -> Any:
        """Retrieve stored memory, loading from DB if necessary."""
        if not self.memory:
            await self._load_memory()
        memory_data = self.memory.get(key)
        return memory_data["value"] if memory_data else default

    async def _update_status(self, new_status: str) -> None:
        """Internal method to update agent status and save to DB."""
        self.agent_instance.status = new_status
        await sync_to_async(self.agent_instance.save)(update_fields=['status'])
        logger.debug(f"Agent {self.name} status changed to: {new_status}")

    async def _log_usage(self) -> None:
        """Internal method to log agent usage and update last_used in DB."""
        self.agent_instance.last_used = timezone.now()
        await sync_to_async(self.agent_instance.save)(update_fields=['last_used'])
        logger.info(f"Agent {self.name} was used at {self.agent_instance.last_used.isoformat()}")

    def __repr__(self) -> str:
        return f"<EnhancedAgent(id={self.agent_instance.id}, name='{self.name}', status='{self.status}')>"

    async def search_knowledge_base(self, query: str, index_name: str = "knowledge_base") -> List[str]:
        """
        Searches the knowledge base for a given query.
        """
        if es_client_module.async_es_client is None:
            logger.error("Elasticsearch client is not available.")
            raise RuntimeError("ES client required for RAG but not available")
            return []

        try:
            response = await es_client_module.async_es_client.search(
                index=index_name,
                body={
                    "query": {
                        "match": {
                            "content": query
                        }
                    }
                }
            )
            return [hit["_source"]["content"] for hit in response["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}", exc_info=True)
            return []
    
    async def handle_task(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """A wrapper method to handle a task with logging, status updates, and validation"""
        await self._load_memory()
        await self._update_status("processing")
        await self._log_usage()
        
        start_time = timezone.now()
        
        if not self.validate_task(task):
            await self._update_status("error")
            return self.format_response(result="Invalid task structure", metadata={"error": "Missing required fields"})
        
        try:
            result = await self.process(task, context)
            await self._save_memory()
            await self._update_status("idle")
            
            end_time = timezone.now()
            duration = (end_time - start_time).total_seconds()
            
            # Log the successful execution
            await sync_to_async(AgentLog.objects.create)(
                agent=self.agent_instance,
                prompt=task.get("prompt", ""),
                response=json.dumps(result),
                status='SUCCESS',
                duration=duration
            )
            
            return self.format_response(result)
        except Exception as e:
            logger.error(f"Error processing task in agent {self.name}: {e}", exc_info=True)
            await self._update_status("error")

            end_time = timezone.now()
            duration = (end_time - start_time).total_seconds()
            
            # Log the error
            await sync_to_async(AgentLog.objects.create)(
                agent=self.agent_instance,
                prompt=task.get("prompt", ""),
                response=json.dumps({"error": str(e)}),
                status='ERROR',
                duration=duration
            )
            
            return self.format_response(result=str(e), metadata={"error": "An unexpected error occurred"})