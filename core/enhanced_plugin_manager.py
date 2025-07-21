import asyncio
import importlib
import os
import time
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from dataclasses import dataclass
import threading
from functools import wraps

from .enhanced_plugin_interface import (
    EnhancedPluginInterface, PluginContext, ExecutionResult, 
    HealthCheckResult, HealthStatus, ExecutionStatus,
    AgentExecutionError, PluginLoadError
)
from .config_manager import SystemConfig

@dataclass
class PluginMetrics:
    """Plugin performance metrics"""
    name: str
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_execution_time_ms: float = 0.0
    last_execution_time: Optional[datetime] = None
    last_health_check_time: Optional[datetime] = None
    last_health_status: HealthStatus = HealthStatus.UNKNOWN

@dataclass
class DependencyNode:
    """Dependency graph node"""
    name: str
    dependencies: Set[str]
    dependents: Set[str]
    resolved: bool = False

def retry(max_attempts: int = 3, backoff_seconds: float = 1.0, exceptions: tuple = (Exception,)):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = backoff_seconds * (2 ** attempt)
                        await asyncio.sleep(wait_time)
                    else:
                        raise last_exception
            return None
        return wrapper
    return decorator

class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        self._lock = threading.Lock()
    
    def call(self, func):
        """Execute function with circuit breaker protection"""
        with self._lock:
            if self.state == "open":
                if self._should_attempt_reset():
                    self.state = "half-open"
                else:
                    raise Exception("Circuit breaker is open")
            
            try:
                result = func()
                self._on_success()
                return result
            except Exception as e:
                self._on_failure()
                raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        return (self.last_failure_time and 
                time.time() - self.last_failure_time > self.recovery_timeout)
    
    def _on_success(self):
        """Handle successful execution"""
        self.failure_count = 0
        self.state = "closed"
    
    def _on_failure(self):
        """Handle failed execution"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"

class EnhancedPluginManager:
    """Professional-grade plugin manager with advanced features"""
    
    def __init__(self, plugin_folder: str, config: SystemConfig):
        self.plugin_folder = plugin_folder
        self.config = config
        self.plugins: Dict[str, EnhancedPluginInterface] = {}
        self.plugin_metrics: Dict[str, PluginMetrics] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.dependency_graph: Dict[str, DependencyNode] = {}
        self.execution_order: List[str] = []
        self.logger = logging.getLogger(__name__)
        self.executor = ThreadPoolExecutor(max_workers=config.max_concurrent_agents)
        self._health_check_task: Optional[asyncio.Task] = None
        self._monitoring_enabled = True
        
    async def initialize(self, context: PluginContext) -> bool:
        """Initialize the plugin manager"""
        try:
            self.logger.info("Initializing Enhanced Plugin Manager...")
            
            # Discover plugins
            await self.discover_plugins()
            
            # Initialize plugins with context
            await self.initialize_plugins(context)
            
            # Build dependency graph
            self.build_dependency_graph()
            
            # Start health monitoring
            if self.config.metrics_enabled:
                await self.start_health_monitoring()
            
            self.logger.info(f"Plugin Manager initialized with {len(self.plugins)} plugins")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Plugin Manager: {e}")
            return False
    
    async def discover_plugins(self):
        """Discover and load plugins asynchronously"""
        plugin_tasks = []
        
        for plugin_name in os.listdir(self.plugin_folder):
            plugin_path = os.path.join(self.plugin_folder, plugin_name)
            if os.path.isdir(plugin_path):
                task = asyncio.create_task(self._load_plugin_async(plugin_name))
                plugin_tasks.append(task)
        
        # Wait for all plugins to load
        results = await asyncio.gather(*plugin_tasks, return_exceptions=True)
        
        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                plugin_name = os.listdir(self.plugin_folder)[i]
                self.logger.error(f"Failed to load plugin {plugin_name}: {result}")
    
    async def _load_plugin_async(self, plugin_name: str):
        """Load a single plugin asynchronously"""
        try:
            # Run plugin loading in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            plugin = await loop.run_in_executor(
                self.executor, 
                self._load_plugin_sync, 
                plugin_name
            )
            
            if plugin:
                self.plugins[plugin.name] = plugin
                self.plugin_metrics[plugin.name] = PluginMetrics(name=plugin.name)
                self.circuit_breakers[plugin.name] = CircuitBreaker()
                self.logger.info(f"Successfully loaded plugin: {plugin.name}")
                
        except Exception as e:
            raise PluginLoadError(f"Failed to load plugin {plugin_name}", plugin_name, e)
    
    def _load_plugin_sync(self, plugin_name: str) -> Optional[EnhancedPluginInterface]:
        """Synchronous plugin loading"""
        try:
            module = importlib.import_module(f"plugins.{plugin_name}")
            plugin = module.get_plugin()
            
            # Validate plugin interface
            if not isinstance(plugin, EnhancedPluginInterface):
                raise TypeError(f"Plugin {plugin_name} does not implement EnhancedPluginInterface")
            
            return plugin
            
        except (ImportError, AttributeError, TypeError) as e:
            self.logger.error(f"Could not load plugin {plugin_name}: {e}")
            return None
    
    async def initialize_plugins(self, context: PluginContext):
        """Initialize all loaded plugins"""
        initialization_tasks = []
        
        for plugin in self.plugins.values():
            task = asyncio.create_task(self._initialize_plugin(plugin, context))
            initialization_tasks.append(task)
        
        results = await asyncio.gather(*initialization_tasks, return_exceptions=True)
        
        # Log initialization results
        for i, result in enumerate(results):
            plugin_name = list(self.plugins.keys())[i]
            if isinstance(result, Exception):
                self.logger.error(f"Failed to initialize plugin {plugin_name}: {result}")
            elif result:
                self.logger.info(f"Successfully initialized plugin: {plugin_name}")
    
    async def _initialize_plugin(self, plugin: EnhancedPluginInterface, context: PluginContext) -> bool:
        """Initialize a single plugin"""
        try:
            # Validate configuration for this plugin
            agent_config = context.config.get(plugin.name, {})
            plugin.validate_configuration(agent_config)
            
            # Initialize plugin
            success = await plugin.initialize(context)
            if success:
                plugin._initialized = True
            
            return success
            
        except Exception as e:
            self.logger.error(f"Plugin {plugin.name} initialization failed: {e}")
            return False
    
    def build_dependency_graph(self):
        """Build dependency resolution graph"""
        self.dependency_graph.clear()
        
        # Create nodes for all plugins
        for plugin_name, plugin in self.plugins.items():
            dependencies = set(plugin.get_dependencies())
            self.dependency_graph[plugin_name] = DependencyNode(
                name=plugin_name,
                dependencies=dependencies,
                dependents=set()
            )
        
        # Build reverse dependencies
        for node_name, node in self.dependency_graph.items():
            for dep_name in node.dependencies:
                if dep_name in self.dependency_graph:
                    self.dependency_graph[dep_name].dependents.add(node_name)
        
        # Resolve execution order using topological sort
        self.execution_order = self._topological_sort()
    
    def _topological_sort(self) -> List[str]:
        """Topological sort for dependency resolution"""
        in_degree = {}
        for node_name, node in self.dependency_graph.items():
            in_degree[node_name] = len(node.dependencies)
        
        queue = [name for name, degree in in_degree.items() if degree == 0]
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            
            if current in self.dependency_graph:
                for dependent in self.dependency_graph[current].dependents:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)
        
        if len(result) != len(self.dependency_graph):
            raise ValueError("Circular dependency detected in plugins")
        
        return result
    
    @retry(max_attempts=3, backoff_seconds=2.0)
    async def run_plugin(self, plugin_name: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Run a specific plugin with retry and circuit breaker"""
        if plugin_name not in self.plugins:
            raise AgentExecutionError(f"Plugin '{plugin_name}' not found", plugin_name)
        
        plugin = self.plugins[plugin_name]
        circuit_breaker = self.circuit_breakers[plugin_name]
        timeout = timeout or self.config.agent_timeout_seconds
        
        start_time = time.time()
        
        try:
            # Execute with circuit breaker protection
            async def execute():
                return await asyncio.wait_for(plugin.run(), timeout=timeout)
            
            result = circuit_breaker.call(lambda: asyncio.run(execute()))
            
            # Update metrics
            execution_time_ms = int((time.time() - start_time) * 1000)
            self._update_metrics(plugin_name, True, execution_time_ms)
            
            return result
            
        except TimeoutError:
            error = AgentExecutionError(f"Plugin {plugin_name} timed out", plugin_name)
            self._update_metrics(plugin_name, False)
            return ExecutionResult(
                status=ExecutionStatus.TIMEOUT,
                error=error,
                execution_time_ms=int((time.time() - start_time) * 1000)
            )
            
        except Exception as e:
            self._update_metrics(plugin_name, False)
            
            # Attempt self-healing if supported
            if hasattr(plugin, 'auto_recover'):
                recovery_success = await plugin.auto_recover(e)
                if recovery_success:
                    self.logger.info(f"Plugin {plugin_name} self-healed successfully")
                    # Retry execution after recovery
                    try:
                        result = await asyncio.wait_for(plugin.run(), timeout=timeout)
                        execution_time_ms = int((time.time() - start_time) * 1000)
                        self._update_metrics(plugin_name, True, execution_time_ms)
                        return result
                    except Exception as retry_error:
                        e = retry_error
            
            raise AgentExecutionError(f"Plugin {plugin_name} execution failed", plugin_name, e)
    
    async def run_all_plugins(self, parallel: bool = True) -> Dict[str, ExecutionResult]:
        """Run all plugins either in parallel or sequential order"""
        if parallel and self.config.max_concurrent_agents > 1:
            return await self._run_plugins_parallel()
        else:
            return await self._run_plugins_sequential()
    
    async def _run_plugins_parallel(self) -> Dict[str, ExecutionResult]:
        """Run plugins in parallel with dependency respect"""
        results = {}
        executed = set()
        
        # Group plugins by dependency levels
        levels = self._get_dependency_levels()
        
        for level_plugins in levels:
            # Run plugins at the same level in parallel
            tasks = []
            for plugin_name in level_plugins:
                if plugin_name not in executed:
                    task = asyncio.create_task(self.run_plugin(plugin_name))
                    tasks.append((plugin_name, task))
            
            # Wait for current level to complete
            for plugin_name, task in tasks:
                try:
                    result = await task
                    results[plugin_name] = result
                    executed.add(plugin_name)
                except Exception as e:
                    results[plugin_name] = ExecutionResult(
                        status=ExecutionStatus.FAILED,
                        error=e
                    )
                    executed.add(plugin_name)
        
        return results
    
    async def _run_plugins_sequential(self) -> Dict[str, ExecutionResult]:
        """Run plugins in dependency order sequentially"""
        results = {}
        
        for plugin_name in self.execution_order:
            try:
                result = await self.run_plugin(plugin_name)
                results[plugin_name] = result
            except Exception as e:
                results[plugin_name] = ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    error=e
                )
        
        return results
    
    def _get_dependency_levels(self) -> List[List[str]]:
        """Get plugins grouped by dependency levels"""
        levels = []
        remaining = set(self.execution_order)
        
        while remaining:
            current_level = []
            for plugin_name in list(remaining):
                dependencies = self.dependency_graph[plugin_name].dependencies
                if dependencies.issubset(set().union(*levels) if levels else set()):
                    current_level.append(plugin_name)
                    remaining.remove(plugin_name)
            
            if not current_level:
                break  # Prevent infinite loop
            
            levels.append(current_level)
        
        return levels
    
    def _update_metrics(self, plugin_name: str, success: bool, execution_time_ms: int = 0):
        """Update plugin metrics"""
        if plugin_name in self.plugin_metrics:
            metrics = self.plugin_metrics[plugin_name]
            metrics.total_executions += 1
            metrics.last_execution_time = datetime.now()
            
            if success:
                metrics.successful_executions += 1
            else:
                metrics.failed_executions += 1
            
            if execution_time_ms > 0:
                # Update average execution time
                total_time = (metrics.average_execution_time_ms * 
                            (metrics.total_executions - 1) + execution_time_ms)
                metrics.average_execution_time_ms = total_time / metrics.total_executions
    
    async def start_health_monitoring(self):
        """Start background health monitoring"""
        if self._health_check_task and not self._health_check_task.done():
            return
        
        self._health_check_task = asyncio.create_task(self._health_monitoring_loop())
    
    async def _health_monitoring_loop(self):
        """Background health monitoring loop"""
        while self._monitoring_enabled:
            try:
                for plugin_name, plugin in self.plugins.items():
                    try:
                        health_result = await plugin.health_check()
                        self.plugin_metrics[plugin_name].last_health_check_time = datetime.now()
                        self.plugin_metrics[plugin_name].last_health_status = health_result.status
                        
                        if health_result.status == HealthStatus.UNHEALTHY:
                            self.logger.warning(f"Plugin {plugin_name} is unhealthy: {health_result.message}")
                            
                    except Exception as e:
                        self.logger.error(f"Health check failed for {plugin_name}: {e}")
                
                await asyncio.sleep(self.config.health_check_interval)
                
            except Exception as e:
                self.logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics"""
        return {
            'total_plugins': len(self.plugins),
            'healthy_plugins': len([m for m in self.plugin_metrics.values() 
                                   if m.last_health_status == HealthStatus.HEALTHY]),
            'plugin_metrics': {name: {
                'total_executions': metrics.total_executions,
                'success_rate': (metrics.successful_executions / metrics.total_executions 
                               if metrics.total_executions > 0 else 0),
                'average_execution_time_ms': metrics.average_execution_time_ms,
                'last_health_status': metrics.last_health_status.value,
                'circuit_breaker_state': self.circuit_breakers[name].state
            } for name, metrics in self.plugin_metrics.items()},
            'dependency_graph': {name: list(node.dependencies) 
                               for name, node in self.dependency_graph.items()},
            'execution_order': self.execution_order
        }
    
    async def shutdown(self):
        """Graceful shutdown of plugin manager"""
        self.logger.info("Shutting down Plugin Manager...")
        
        # Stop health monitoring
        self._monitoring_enabled = False
        if self._health_check_task:
            self._health_check_task.cancel()
        
        # Shutdown all plugins
        shutdown_tasks = []
        for plugin in self.plugins.values():
            task = asyncio.create_task(plugin.shutdown())
            shutdown_tasks.append(task)
        
        await asyncio.gather(*shutdown_tasks, return_exceptions=True)
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        self.logger.info("Plugin Manager shutdown complete")
