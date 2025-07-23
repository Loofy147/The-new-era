from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class ExecutionStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

@dataclass
class PluginContext:
    """Context provided to plugins for dependency injection"""
    config: Dict[str, Any]
    logger: Any
    metrics_collector: Any
    event_bus: Any
    storage: Any
    cache: Any

@dataclass
class ExecutionResult:
    """Standardized execution result"""
    status: ExecutionStatus
    data: Optional[Dict[str, Any]] = None
    error: Optional[Exception] = None
    execution_time_ms: Optional[int] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class HealthCheckResult:
    """Health check result with detailed status"""
    status: HealthStatus
    message: str
    details: Dict[str, Any] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.details is None:
            self.details = {}

class AgentExecutionError(Exception):
    """Custom exception for agent execution failures"""
    def __init__(self, message: str, agent_name: str, original_error: Exception = None):
        super().__init__(message)
        self.agent_name = agent_name
        self.original_error = original_error

class PluginLoadError(Exception):
    """Custom exception for plugin loading failures"""
    def __init__(self, message: str, plugin_name: str, original_error: Exception = None):
        super().__init__(message)
        self.plugin_name = plugin_name
        self.original_error = original_error

class ConfigValidationError(Exception):
    """Custom exception for configuration validation failures"""
    pass

class EnhancedPluginInterface(ABC):
    """Enhanced plugin interface with professional standards"""
    
    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.context: Optional[PluginContext] = None
        self._initialized = False
        self._last_health_check: Optional[HealthCheckResult] = None

    @abstractmethod
    async def initialize(self, context: PluginContext) -> bool:
        """Initialize the plugin with provided context"""
        pass

    @abstractmethod
    async def run(self) -> ExecutionResult:
        """Execute the plugin's main functionality"""
        pass

    @abstractmethod
    async def health_check(self) -> HealthCheckResult:
        """Perform health check and return status"""
        pass

    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """Return list of required dependencies"""
        pass

    @abstractmethod
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Return JSON schema for configuration validation"""
        pass

    async def shutdown(self) -> bool:
        """Graceful shutdown of the plugin"""
        try:
            # Default implementation - can be overridden
            if hasattr(self, '_cleanup'):
                await self._cleanup()
            return True
        except Exception as e:
            if self.context and self.context.logger:
                self.context.logger.error(f"Error during shutdown of {self.name}: {e}")
            return False

    def validate_configuration(self, config: Dict[str, Any]) -> bool:
        """Validate configuration against schema"""
        schema = self.get_configuration_schema()
        # Basic validation - can be enhanced with jsonschema
        for key, spec in schema.items():
            if spec.get('required', False) and key not in config:
                raise ConfigValidationError(f"Required configuration key '{key}' missing for {self.name}")
        return True

    async def get_metrics(self) -> Dict[str, Any]:
        """Get performance and operational metrics"""
        return {
            'name': self.name,
            'status': 'initialized' if self._initialized else 'not_initialized',
            'last_health_check': self._last_health_check.status.value if self._last_health_check else 'never',
            'dependencies_satisfied': await self._check_dependencies()
        }

    async def _check_dependencies(self) -> bool:
        """Check if all dependencies are available"""
        dependencies = self.get_dependencies()
        # Implementation would check actual dependency availability
        return True  # Placeholder

    def log_info(self, message: str, **kwargs):
        """Structured logging helper"""
        if self.context and self.context.logger:
            self.context.logger.info(message, agent=self.name, **kwargs)

    def log_error(self, message: str, error: Exception = None, **kwargs):
        """Structured error logging helper"""
        if self.context and self.context.logger:
            self.context.logger.error(message, agent=self.name, error=str(error), **kwargs)

    def emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to event bus"""
        if self.context and self.context.event_bus:
            self.context.event_bus.emit(event_type, {
                'agent': self.name,
                'timestamp': datetime.now().isoformat(),
                'data': data
            })

class SelfHealingMixin:
    """Mixin for self-healing capabilities"""
    
    async def auto_recover(self, error: Exception) -> bool:
        """Attempt automatic recovery from errors"""
        try:
            # Implement recovery strategies
            recovery_strategies = [
                self._restart_components,
                self._clear_cache,
                self._reset_connections,
                self._fallback_mode
            ]
            
            for strategy in recovery_strategies:
                if await strategy(error):
                    self.log_info(f"Successfully recovered using {strategy.__name__}")
                    return True
                    
            return False
        except Exception as recovery_error:
            self.log_error(f"Recovery failed: {recovery_error}")
            return False

    async def _restart_components(self, error: Exception) -> bool:
        """Restart internal components"""
        # Implementation specific to each agent
        return False

    async def _clear_cache(self, error: Exception) -> bool:
        """Clear internal caches"""
        # Implementation specific to each agent
        return False

    async def _reset_connections(self, error: Exception) -> bool:
        """Reset external connections"""
        # Implementation specific to each agent
        return False

    async def _fallback_mode(self, error: Exception) -> bool:
        """Enter fallback/safe mode"""
        # Implementation specific to each agent
        return False

class MultiModalCapability:
    """Mixin for multi-modal agent capabilities"""
    
    @abstractmethod
    def get_supported_modalities(self) -> List[str]:
        """Return list of supported modalities (text, voice, image, video, etc.)"""
        pass

    @abstractmethod
    async def process_modality(self, modality: str, data: Any) -> Any:
        """Process data for specific modality"""
        pass

    async def cross_modal_fusion(self, modal_data: Dict[str, Any]) -> Any:
        """Fuse information from multiple modalities"""
        # Default implementation - override for specific fusion strategies
        return modal_data

class VoiceCapability:
    """Mixin for voice-enabled agents"""
    
    @abstractmethod
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text"""
        pass

    @abstractmethod
    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech"""
        pass

    @abstractmethod
    async def process_voice_command(self, command: str) -> ExecutionResult:
        """Process voice command"""
        pass
