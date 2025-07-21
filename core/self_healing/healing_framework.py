import asyncio
import logging
import json
import time
import traceback
from typing import Dict, List, Any, Optional, Callable, Type
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from abc import ABC, abstractmethod
import threading
from pathlib import Path

class FailureType(Enum):
    """Types of failures that can occur"""
    EXECUTION_ERROR = "execution_error"
    TIMEOUT = "timeout"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    DEPENDENCY_FAILURE = "dependency_failure"
    CONFIGURATION_ERROR = "configuration_error"
    NETWORK_ERROR = "network_error"
    AUTHENTICATION_ERROR = "authentication_error"
    DATA_CORRUPTION = "data_corruption"
    MEMORY_LEAK = "memory_leak"
    UNKNOWN = "unknown"

class RecoveryStrategy(Enum):
    """Recovery strategies available"""
    RESTART = "restart"
    ROLLBACK = "rollback"
    RETRY = "retry"
    FALLBACK = "fallback"
    RECONFIGURE = "reconfigure"
    RESET_STATE = "reset_state"
    ESCALATE = "escalate"
    ISOLATE = "isolate"

@dataclass
class FailureEvent:
    """Represents a failure event"""
    id: str
    agent_name: str
    failure_type: FailureType
    error_message: str
    stack_trace: str
    timestamp: datetime
    severity: str  # critical, high, medium, low
    context: Dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolution_strategy: Optional[RecoveryStrategy] = None
    resolution_time: Optional[datetime] = None

@dataclass
class RecoveryAction:
    """Represents a recovery action"""
    id: str
    strategy: RecoveryStrategy
    description: str
    agent_name: str
    timestamp: datetime
    success: bool = False
    execution_time_ms: int = 0
    side_effects: List[str] = field(default_factory=list)

@dataclass
class HealthMetrics:
    """Health metrics for an agent"""
    agent_name: str
    last_health_check: datetime
    consecutive_failures: int = 0
    total_failures: int = 0
    total_recoveries: int = 0
    success_rate: float = 1.0
    average_response_time_ms: float = 0.0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    last_successful_execution: Optional[datetime] = None

class RecoveryHandler(ABC):
    """Abstract base class for recovery handlers"""
    
    @abstractmethod
    async def can_handle(self, failure: FailureEvent) -> bool:
        """Check if this handler can address the failure"""
        pass
    
    @abstractmethod
    async def recover(self, failure: FailureEvent, context: Dict[str, Any]) -> RecoveryAction:
        """Execute recovery action"""
        pass
    
    @abstractmethod
    def get_strategy(self) -> RecoveryStrategy:
        """Get the recovery strategy this handler implements"""
        pass

class RestartRecoveryHandler(RecoveryHandler):
    """Handler for restart-based recovery"""
    
    async def can_handle(self, failure: FailureEvent) -> bool:
        return failure.failure_type in [
            FailureType.EXECUTION_ERROR,
            FailureType.MEMORY_LEAK,
            FailureType.TIMEOUT
        ]
    
    async def recover(self, failure: FailureEvent, context: Dict[str, Any]) -> RecoveryAction:
        action = RecoveryAction(
            id=f"restart_{failure.id}",
            strategy=RecoveryStrategy.RESTART,
            description=f"Restarting agent {failure.agent_name}",
            agent_name=failure.agent_name,
            timestamp=datetime.now()
        )
        
        start_time = time.time()
        
        try:
            # Get agent instance from context
            agent = context.get('agent')
            if agent:
                # Graceful shutdown
                await agent.shutdown()
                await asyncio.sleep(1)
                
                # Reinitialize
                success = await agent.initialize(context.get('plugin_context'))
                
                action.success = success
                action.execution_time_ms = int((time.time() - start_time) * 1000)
                
                if success:
                    action.side_effects.append("Agent successfully restarted")
                else:
                    action.side_effects.append("Agent restart failed")
            else:
                action.success = False
                action.side_effects.append("Agent instance not available for restart")
                
        except Exception as e:
            action.success = False
            action.side_effects.append(f"Restart failed: {str(e)}")
            action.execution_time_ms = int((time.time() - start_time) * 1000)
        
        return action
    
    def get_strategy(self) -> RecoveryStrategy:
        return RecoveryStrategy.RESTART

class RetryRecoveryHandler(RecoveryHandler):
    """Handler for retry-based recovery"""
    
    def __init__(self, max_retries: int = 3, backoff_seconds: float = 2.0):
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds
    
    async def can_handle(self, failure: FailureEvent) -> bool:
        return failure.failure_type in [
            FailureType.NETWORK_ERROR,
            FailureType.TIMEOUT,
            FailureType.DEPENDENCY_FAILURE
        ]
    
    async def recover(self, failure: FailureEvent, context: Dict[str, Any]) -> RecoveryAction:
        action = RecoveryAction(
            id=f"retry_{failure.id}",
            strategy=RecoveryStrategy.RETRY,
            description=f"Retrying operation for agent {failure.agent_name}",
            agent_name=failure.agent_name,
            timestamp=datetime.now()
        )
        
        start_time = time.time()
        
        try:
            agent = context.get('agent')
            original_operation = context.get('original_operation')
            
            if agent and original_operation:
                for attempt in range(self.max_retries):
                    try:
                        await asyncio.sleep(self.backoff_seconds * (attempt + 1))
                        result = await original_operation()
                        
                        action.success = True
                        action.side_effects.append(f"Operation succeeded on attempt {attempt + 1}")
                        break
                        
                    except Exception as e:
                        if attempt == self.max_retries - 1:
                            action.success = False
                            action.side_effects.append(f"All {self.max_retries} retry attempts failed")
                        else:
                            action.side_effects.append(f"Attempt {attempt + 1} failed: {str(e)}")
            else:
                action.success = False
                action.side_effects.append("Agent or operation not available for retry")
                
        except Exception as e:
            action.success = False
            action.side_effects.append(f"Retry handler failed: {str(e)}")
        
        action.execution_time_ms = int((time.time() - start_time) * 1000)
        return action
    
    def get_strategy(self) -> RecoveryStrategy:
        return RecoveryStrategy.RETRY

class FallbackRecoveryHandler(RecoveryHandler):
    """Handler for fallback recovery strategies"""
    
    async def can_handle(self, failure: FailureEvent) -> bool:
        return failure.failure_type in [
            FailureType.DEPENDENCY_FAILURE,
            FailureType.CONFIGURATION_ERROR,
            FailureType.AUTHENTICATION_ERROR
        ]
    
    async def recover(self, failure: FailureEvent, context: Dict[str, Any]) -> RecoveryAction:
        action = RecoveryAction(
            id=f"fallback_{failure.id}",
            strategy=RecoveryStrategy.FALLBACK,
            description=f"Activating fallback mode for agent {failure.agent_name}",
            agent_name=failure.agent_name,
            timestamp=datetime.now()
        )
        
        start_time = time.time()
        
        try:
            agent = context.get('agent')
            
            if agent and hasattr(agent, 'enter_fallback_mode'):
                success = await agent.enter_fallback_mode(failure)
                action.success = success
                
                if success:
                    action.side_effects.append("Agent entered fallback mode successfully")
                else:
                    action.side_effects.append("Failed to enter fallback mode")
            else:
                # Generic fallback: reduce functionality
                action.success = True
                action.side_effects.append("Applied generic fallback strategy")
                
        except Exception as e:
            action.success = False
            action.side_effects.append(f"Fallback activation failed: {str(e)}")
        
        action.execution_time_ms = int((time.time() - start_time) * 1000)
        return action
    
    def get_strategy(self) -> RecoveryStrategy:
        return RecoveryStrategy.FALLBACK

class ReconfigurationRecoveryHandler(RecoveryHandler):
    """Handler for configuration-based recovery"""
    
    async def can_handle(self, failure: FailureEvent) -> bool:
        return failure.failure_type in [
            FailureType.CONFIGURATION_ERROR,
            FailureType.AUTHENTICATION_ERROR
        ]
    
    async def recover(self, failure: FailureEvent, context: Dict[str, Any]) -> RecoveryAction:
        action = RecoveryAction(
            id=f"reconfig_{failure.id}",
            strategy=RecoveryStrategy.RECONFIGURE,
            description=f"Reconfiguring agent {failure.agent_name}",
            agent_name=failure.agent_name,
            timestamp=datetime.now()
        )
        
        start_time = time.time()
        
        try:
            # Attempt to reload configuration
            config_manager = context.get('config_manager')
            agent = context.get('agent')
            
            if config_manager and agent:
                # Get fresh configuration
                new_config = config_manager.get_agent_config(failure.agent_name)
                
                # Apply new configuration
                if hasattr(agent, 'reconfigure'):
                    success = await agent.reconfigure(new_config)
                    action.success = success
                    
                    if success:
                        action.side_effects.append("Agent reconfigured successfully")
                    else:
                        action.side_effects.append("Agent reconfiguration failed")
                else:
                    action.success = False
                    action.side_effects.append("Agent does not support reconfiguration")
            else:
                action.success = False
                action.side_effects.append("Configuration manager or agent not available")
                
        except Exception as e:
            action.success = False
            action.side_effects.append(f"Reconfiguration failed: {str(e)}")
        
        action.execution_time_ms = int((time.time() - start_time) * 1000)
        return action
    
    def get_strategy(self) -> RecoveryStrategy:
        return RecoveryStrategy.RECONFIGURE

class StateResetRecoveryHandler(RecoveryHandler):
    """Handler for state reset recovery"""
    
    async def can_handle(self, failure: FailureEvent) -> bool:
        return failure.failure_type in [
            FailureType.DATA_CORRUPTION,
            FailureType.MEMORY_LEAK
        ]
    
    async def recover(self, failure: FailureEvent, context: Dict[str, Any]) -> RecoveryAction:
        action = RecoveryAction(
            id=f"reset_state_{failure.id}",
            strategy=RecoveryStrategy.RESET_STATE,
            description=f"Resetting state for agent {failure.agent_name}",
            agent_name=failure.agent_name,
            timestamp=datetime.now()
        )
        
        start_time = time.time()
        
        try:
            agent = context.get('agent')
            
            if agent and hasattr(agent, 'reset_state'):
                success = await agent.reset_state()
                action.success = success
                
                if success:
                    action.side_effects.append("Agent state reset successfully")
                else:
                    action.side_effects.append("Agent state reset failed")
            else:
                # Generic state reset
                action.success = True
                action.side_effects.append("Applied generic state reset")
                
        except Exception as e:
            action.success = False
            action.side_effects.append(f"State reset failed: {str(e)}")
        
        action.execution_time_ms = int((time.time() - start_time) * 1000)
        return action
    
    def get_strategy(self) -> RecoveryStrategy:
        return RecoveryStrategy.RESET_STATE

class SelfHealingFramework:
    """Autonomous self-healing framework for agents"""
    
    def __init__(self, data_dir: str = "data/self_healing"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.failure_history: List[FailureEvent] = []
        self.recovery_history: List[RecoveryAction] = []
        self.health_metrics: Dict[str, HealthMetrics] = {}
        
        self.recovery_handlers: List[RecoveryHandler] = [
            RestartRecoveryHandler(),
            RetryRecoveryHandler(),
            FallbackRecoveryHandler(),
            ReconfigurationRecoveryHandler(),
            StateResetRecoveryHandler()
        ]
        
        self.logger = logging.getLogger(__name__)
        self.monitoring_enabled = True
        self.monitoring_task: Optional[asyncio.Task] = None
        
        # Configuration
        self.max_consecutive_failures = 5
        self.failure_window_minutes = 60
        self.health_check_interval_seconds = 30
        
        # Load historical data
        self._load_historical_data()
    
    def _load_historical_data(self):
        """Load historical failure and recovery data"""
        try:
            # Load failure history
            failure_file = self.data_dir / "failure_history.json"
            if failure_file.exists():
                with open(failure_file, 'r') as f:
                    data = json.load(f)
                
                for failure_data in data.get('failures', []):
                    failure = FailureEvent(
                        id=failure_data['id'],
                        agent_name=failure_data['agent_name'],
                        failure_type=FailureType(failure_data['failure_type']),
                        error_message=failure_data['error_message'],
                        stack_trace=failure_data['stack_trace'],
                        timestamp=datetime.fromisoformat(failure_data['timestamp']),
                        severity=failure_data['severity'],
                        context=failure_data.get('context', {}),
                        resolved=failure_data.get('resolved', False),
                        resolution_strategy=RecoveryStrategy(failure_data['resolution_strategy']) if failure_data.get('resolution_strategy') else None,
                        resolution_time=datetime.fromisoformat(failure_data['resolution_time']) if failure_data.get('resolution_time') else None
                    )
                    self.failure_history.append(failure)
            
            # Load recovery history
            recovery_file = self.data_dir / "recovery_history.json"
            if recovery_file.exists():
                with open(recovery_file, 'r') as f:
                    data = json.load(f)
                
                for recovery_data in data.get('recoveries', []):
                    recovery = RecoveryAction(
                        id=recovery_data['id'],
                        strategy=RecoveryStrategy(recovery_data['strategy']),
                        description=recovery_data['description'],
                        agent_name=recovery_data['agent_name'],
                        timestamp=datetime.fromisoformat(recovery_data['timestamp']),
                        success=recovery_data['success'],
                        execution_time_ms=recovery_data['execution_time_ms'],
                        side_effects=recovery_data.get('side_effects', [])
                    )
                    self.recovery_history.append(recovery)
            
            self.logger.info(f"Loaded {len(self.failure_history)} failure events and {len(self.recovery_history)} recovery actions")
            
        except Exception as e:
            self.logger.error(f"Failed to load historical data: {e}")
    
    async def register_failure(self, agent_name: str, error: Exception, 
                             context: Dict[str, Any] = None) -> FailureEvent:
        """Register a failure event and trigger recovery"""
        failure_type = self._classify_failure(error)
        severity = self._assess_severity(agent_name, failure_type)
        
        failure = FailureEvent(
            id=f"failure_{len(self.failure_history)}_{int(time.time())}",
            agent_name=agent_name,
            failure_type=failure_type,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            timestamp=datetime.now(),
            severity=severity,
            context=context or {}
        )
        
        self.failure_history.append(failure)
        
        # Update health metrics
        self._update_health_metrics(agent_name, success=False)
        
        # Log the failure
        self.logger.error(f"Failure registered for {agent_name}: {failure.error_message}")
        
        # Trigger automatic recovery
        await self._trigger_recovery(failure, context or {})
        
        # Save updated data
        await self._save_historical_data()
        
        return failure
    
    def _classify_failure(self, error: Exception) -> FailureType:
        """Classify the type of failure based on the error"""
        error_message = str(error).lower()
        error_type = type(error).__name__.lower()
        
        if 'timeout' in error_message or 'timeout' in error_type:
            return FailureType.TIMEOUT
        elif 'network' in error_message or 'connection' in error_message:
            return FailureType.NETWORK_ERROR
        elif 'memory' in error_message or 'outofmemory' in error_type:
            return FailureType.MEMORY_LEAK
        elif 'authentication' in error_message or 'unauthorized' in error_message:
            return FailureType.AUTHENTICATION_ERROR
        elif 'config' in error_message or 'setting' in error_message:
            return FailureType.CONFIGURATION_ERROR
        elif 'dependency' in error_message or 'import' in error_message:
            return FailureType.DEPENDENCY_FAILURE
        elif 'corrupt' in error_message or 'invalid' in error_message:
            return FailureType.DATA_CORRUPTION
        elif 'resource' in error_message or 'disk' in error_message:
            return FailureType.RESOURCE_EXHAUSTION
        else:
            return FailureType.EXECUTION_ERROR
    
    def _assess_severity(self, agent_name: str, failure_type: FailureType) -> str:
        """Assess the severity of a failure"""
        # Get recent failures for this agent
        recent_failures = self._get_recent_failures(agent_name)
        
        # Critical severity conditions
        if len(recent_failures) >= self.max_consecutive_failures:
            return "critical"
        
        if failure_type in [FailureType.DATA_CORRUPTION, FailureType.MEMORY_LEAK]:
            return "critical"
        
        # High severity conditions
        if failure_type in [FailureType.AUTHENTICATION_ERROR, FailureType.RESOURCE_EXHAUSTION]:
            return "high"
        
        if len(recent_failures) >= 3:
            return "high"
        
        # Medium severity conditions
        if failure_type in [FailureType.NETWORK_ERROR, FailureType.DEPENDENCY_FAILURE]:
            return "medium"
        
        # Default to low severity
        return "low"
    
    def _get_recent_failures(self, agent_name: str, window_minutes: int = None) -> List[FailureEvent]:
        """Get recent failures for an agent within a time window"""
        if window_minutes is None:
            window_minutes = self.failure_window_minutes
        
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        
        return [
            failure for failure in self.failure_history
            if (failure.agent_name == agent_name and 
                failure.timestamp >= cutoff_time and
                not failure.resolved)
        ]
    
    async def _trigger_recovery(self, failure: FailureEvent, context: Dict[str, Any]):
        """Trigger appropriate recovery action"""
        # Find suitable recovery handler
        suitable_handlers = []
        for handler in self.recovery_handlers:
            if await handler.can_handle(failure):
                suitable_handlers.append(handler)
        
        if not suitable_handlers:
            self.logger.warning(f"No recovery handler found for failure {failure.id}")
            return
        
        # Choose best handler based on historical success
        best_handler = self._choose_best_handler(suitable_handlers, failure.agent_name)
        
        # Execute recovery
        try:
            recovery_action = await best_handler.recover(failure, context)
            self.recovery_history.append(recovery_action)
            
            if recovery_action.success:
                failure.resolved = True
                failure.resolution_strategy = recovery_action.strategy
                failure.resolution_time = recovery_action.timestamp
                
                self.logger.info(f"Recovery successful for {failure.agent_name} using {recovery_action.strategy.value}")
                
                # Update health metrics
                self._update_health_metrics(failure.agent_name, success=True, recovery=True)
            else:
                self.logger.error(f"Recovery failed for {failure.agent_name} using {recovery_action.strategy.value}")
                
                # Try escalation if this was not already an escalated recovery
                if recovery_action.strategy != RecoveryStrategy.ESCALATE:
                    await self._escalate_recovery(failure, context)
                    
        except Exception as e:
            self.logger.error(f"Recovery execution failed: {e}")
            await self._escalate_recovery(failure, context)
    
    def _choose_best_handler(self, handlers: List[RecoveryHandler], agent_name: str) -> RecoveryHandler:
        """Choose the best recovery handler based on historical success"""
        if len(handlers) == 1:
            return handlers[0]
        
        # Calculate success rates for each handler strategy
        strategy_success_rates = {}
        
        for handler in handlers:
            strategy = handler.get_strategy()
            
            # Get historical recovery actions for this strategy and agent
            relevant_actions = [
                action for action in self.recovery_history
                if (action.strategy == strategy and 
                    action.agent_name == agent_name)
            ]
            
            if relevant_actions:
                success_rate = sum(1 for action in relevant_actions if action.success) / len(relevant_actions)
            else:
                # Default success rate for unknown strategies
                success_rate = 0.5
            
            strategy_success_rates[handler] = success_rate
        
        # Return handler with highest success rate
        return max(handlers, key=lambda h: strategy_success_rates[h])
    
    async def _escalate_recovery(self, failure: FailureEvent, context: Dict[str, Any]):
        """Escalate recovery when normal strategies fail"""
        escalation_action = RecoveryAction(
            id=f"escalate_{failure.id}",
            strategy=RecoveryStrategy.ESCALATE,
            description=f"Escalating recovery for agent {failure.agent_name}",
            agent_name=failure.agent_name,
            timestamp=datetime.now()
        )
        
        try:
            # Multiple escalation strategies
            escalation_success = False
            
            # 1. Try isolation
            if await self._isolate_agent(failure.agent_name, context):
                escalation_action.side_effects.append("Agent isolated successfully")
                escalation_success = True
            
            # 2. Notify administrators
            await self._notify_administrators(failure)
            escalation_action.side_effects.append("Administrators notified")
            
            # 3. Create incident report
            incident_report = await self._create_incident_report(failure)
            escalation_action.side_effects.append(f"Incident report created: {incident_report}")
            
            escalation_action.success = escalation_success
            
        except Exception as e:
            escalation_action.success = False
            escalation_action.side_effects.append(f"Escalation failed: {str(e)}")
        
        self.recovery_history.append(escalation_action)
    
    async def _isolate_agent(self, agent_name: str, context: Dict[str, Any]) -> bool:
        """Isolate a failing agent to prevent system-wide issues"""
        try:
            agent = context.get('agent')
            if agent and hasattr(agent, 'isolate'):
                return await agent.isolate()
            else:
                # Generic isolation: remove from active agents
                self.logger.warning(f"Agent {agent_name} isolated due to repeated failures")
                return True
        except Exception as e:
            self.logger.error(f"Failed to isolate agent {agent_name}: {e}")
            return False
    
    async def _notify_administrators(self, failure: FailureEvent):
        """Notify system administrators of critical failures"""
        notification = {
            'type': 'critical_failure',
            'agent_name': failure.agent_name,
            'failure_type': failure.failure_type.value,
            'error_message': failure.error_message,
            'timestamp': failure.timestamp.isoformat(),
            'severity': failure.severity
        }
        
        # Save notification (in production, this would send emails/alerts)
        notifications_file = self.data_dir / "admin_notifications.json"
        notifications = []
        
        if notifications_file.exists():
            with open(notifications_file, 'r') as f:
                notifications = json.load(f)
        
        notifications.append(notification)
        
        with open(notifications_file, 'w') as f:
            json.dump(notifications, f, indent=2)
        
        self.logger.critical(f"Administrator notification sent for {failure.agent_name}")
    
    async def _create_incident_report(self, failure: FailureEvent) -> str:
        """Create detailed incident report"""
        incident_id = f"incident_{failure.id}_{int(time.time())}"
        
        # Get related failures
        related_failures = self._get_recent_failures(failure.agent_name)
        
        # Get recovery attempts
        related_recoveries = [
            action for action in self.recovery_history
            if action.agent_name == failure.agent_name
        ]
        
        incident_report = {
            'incident_id': incident_id,
            'primary_failure': {
                'id': failure.id,
                'agent_name': failure.agent_name,
                'failure_type': failure.failure_type.value,
                'error_message': failure.error_message,
                'timestamp': failure.timestamp.isoformat(),
                'severity': failure.severity
            },
            'related_failures': [
                {
                    'id': f.id,
                    'failure_type': f.failure_type.value,
                    'timestamp': f.timestamp.isoformat(),
                    'resolved': f.resolved
                }
                for f in related_failures
            ],
            'recovery_attempts': [
                {
                    'id': r.id,
                    'strategy': r.strategy.value,
                    'success': r.success,
                    'timestamp': r.timestamp.isoformat(),
                    'execution_time_ms': r.execution_time_ms
                }
                for r in related_recoveries[-5:]  # Last 5 attempts
            ],
            'health_metrics': self.health_metrics.get(failure.agent_name, {}).__dict__ if failure.agent_name in self.health_metrics else {},
            'created_at': datetime.now().isoformat()
        }
        
        # Save incident report
        incident_file = self.data_dir / f"incident_{incident_id}.json"
        with open(incident_file, 'w') as f:
            json.dump(incident_report, f, indent=2)
        
        return incident_id
    
    def _update_health_metrics(self, agent_name: str, success: bool, recovery: bool = False):
        """Update health metrics for an agent"""
        if agent_name not in self.health_metrics:
            self.health_metrics[agent_name] = HealthMetrics(
                agent_name=agent_name,
                last_health_check=datetime.now()
            )
        
        metrics = self.health_metrics[agent_name]
        metrics.last_health_check = datetime.now()
        
        if success:
            metrics.consecutive_failures = 0
            metrics.last_successful_execution = datetime.now()
            if recovery:
                metrics.total_recoveries += 1
        else:
            metrics.consecutive_failures += 1
            metrics.total_failures += 1
        
        # Update success rate
        total_attempts = metrics.total_failures + (metrics.total_recoveries * 2)  # Recoveries count as attempts
        if total_attempts > 0:
            successful_attempts = total_attempts - metrics.total_failures
            metrics.success_rate = successful_attempts / total_attempts
    
    async def start_monitoring(self):
        """Start continuous health monitoring"""
        if self.monitoring_task and not self.monitoring_task.done():
            return
        
        self.monitoring_enabled = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    async def _monitoring_loop(self):
        """Continuous monitoring loop"""
        while self.monitoring_enabled:
            try:
                # Check health of all agents
                for agent_name, metrics in self.health_metrics.items():
                    await self._check_agent_health(agent_name, metrics)
                
                # Cleanup old data
                await self._cleanup_old_data()
                
                await asyncio.sleep(self.health_check_interval_seconds)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _check_agent_health(self, agent_name: str, metrics: HealthMetrics):
        """Check health of a specific agent"""
        # Check if agent has been failing too frequently
        if metrics.consecutive_failures >= self.max_consecutive_failures:
            self.logger.warning(f"Agent {agent_name} has {metrics.consecutive_failures} consecutive failures")
        
        # Check if agent hasn't been successful recently
        if metrics.last_successful_execution:
            time_since_success = datetime.now() - metrics.last_successful_execution
            if time_since_success.total_seconds() > 3600:  # 1 hour
                self.logger.warning(f"Agent {agent_name} has not succeeded in {time_since_success.total_seconds()/60:.1f} minutes")
    
    async def _cleanup_old_data(self):
        """Clean up old failure and recovery data"""
        cutoff_time = datetime.now() - timedelta(days=30)  # Keep 30 days of data
        
        # Remove old failures
        self.failure_history = [
            failure for failure in self.failure_history
            if failure.timestamp >= cutoff_time
        ]
        
        # Remove old recoveries
        self.recovery_history = [
            recovery for recovery in self.recovery_history
            if recovery.timestamp >= cutoff_time
        ]
    
    async def _save_historical_data(self):
        """Save failure and recovery history to files"""
        try:
            # Save failure history
            failure_data = {
                'failures': [
                    {
                        'id': f.id,
                        'agent_name': f.agent_name,
                        'failure_type': f.failure_type.value,
                        'error_message': f.error_message,
                        'stack_trace': f.stack_trace,
                        'timestamp': f.timestamp.isoformat(),
                        'severity': f.severity,
                        'context': f.context,
                        'resolved': f.resolved,
                        'resolution_strategy': f.resolution_strategy.value if f.resolution_strategy else None,
                        'resolution_time': f.resolution_time.isoformat() if f.resolution_time else None
                    }
                    for f in self.failure_history
                ]
            }
            
            failure_file = self.data_dir / "failure_history.json"
            with open(failure_file, 'w') as f:
                json.dump(failure_data, f, indent=2)
            
            # Save recovery history
            recovery_data = {
                'recoveries': [
                    {
                        'id': r.id,
                        'strategy': r.strategy.value,
                        'description': r.description,
                        'agent_name': r.agent_name,
                        'timestamp': r.timestamp.isoformat(),
                        'success': r.success,
                        'execution_time_ms': r.execution_time_ms,
                        'side_effects': r.side_effects
                    }
                    for r in self.recovery_history
                ]
            }
            
            recovery_file = self.data_dir / "recovery_history.json"
            with open(recovery_file, 'w') as f:
                json.dump(recovery_data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save historical data: {e}")
    
    async def get_system_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report"""
        total_failures = len(self.failure_history)
        resolved_failures = len([f for f in self.failure_history if f.resolved])
        total_recoveries = len(self.recovery_history)
        successful_recoveries = len([r for r in self.recovery_history if r.success])
        
        # Calculate recovery success rate by strategy
        strategy_stats = {}
        for strategy in RecoveryStrategy:
            strategy_recoveries = [r for r in self.recovery_history if r.strategy == strategy]
            if strategy_recoveries:
                success_rate = sum(1 for r in strategy_recoveries if r.success) / len(strategy_recoveries)
                strategy_stats[strategy.value] = {
                    'total_attempts': len(strategy_recoveries),
                    'success_rate': success_rate,
                    'average_execution_time_ms': sum(r.execution_time_ms for r in strategy_recoveries) / len(strategy_recoveries)
                }
        
        # Agent-specific health
        agent_health = {}
        for agent_name, metrics in self.health_metrics.items():
            agent_health[agent_name] = {
                'consecutive_failures': metrics.consecutive_failures,
                'total_failures': metrics.total_failures,
                'total_recoveries': metrics.total_recoveries,
                'success_rate': metrics.success_rate,
                'last_successful_execution': metrics.last_successful_execution.isoformat() if metrics.last_successful_execution else None,
                'status': 'healthy' if metrics.consecutive_failures == 0 else 'degraded' if metrics.consecutive_failures < 3 else 'critical'
            }
        
        return {
            'system_overview': {
                'total_failures': total_failures,
                'resolved_failures': resolved_failures,
                'resolution_rate': resolved_failures / total_failures if total_failures > 0 else 1.0,
                'total_recoveries': total_recoveries,
                'successful_recoveries': successful_recoveries,
                'recovery_success_rate': successful_recoveries / total_recoveries if total_recoveries > 0 else 0.0
            },
            'recovery_strategies': strategy_stats,
            'agent_health': agent_health,
            'monitoring_status': {
                'enabled': self.monitoring_enabled,
                'health_check_interval_seconds': self.health_check_interval_seconds,
                'last_monitoring_run': datetime.now().isoformat()
            },
            'report_generated_at': datetime.now().isoformat()
        }
    
    async def shutdown(self):
        """Shutdown the self-healing framework"""
        self.logger.info("Shutting down self-healing framework...")
        
        self.monitoring_enabled = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
        
        await self._save_historical_data()
        
        self.logger.info("Self-healing framework shutdown complete")

# Global self-healing framework instance
self_healing_framework = SelfHealingFramework()
