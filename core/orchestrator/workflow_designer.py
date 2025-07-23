"""
Advanced Workflow Designer for AI Orchestrator System
Handles intelligent workflow creation, optimization, and adaptive execution patterns.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import uuid
import networkx as nx
from abc import ABC, abstractmethod

class WorkflowType(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    PIPELINE = "pipeline"
    HYBRID = "hybrid"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELLED = "cancelled"

@dataclass
class WorkflowNode:
    """Represents a single node in the workflow graph."""
    id: str
    name: str
    task_type: str
    agent_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.MEDIUM
    estimated_duration: int = 60  # seconds
    timeout: int = 300  # seconds
    retry_count: int = 3
    conditions: Dict[str, Any] = field(default_factory=dict)
    parallel_group: Optional[str] = None
    resource_requirements: Dict[str, Any] = field(default_factory=dict)

@dataclass
class WorkflowExecution:
    """Tracks workflow execution state and metrics."""
    workflow_id: str
    execution_id: str
    status: ExecutionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    current_node: Optional[str] = None
    completed_nodes: Set[str] = field(default_factory=set)
    failed_nodes: Set[str] = field(default_factory=set)
    execution_path: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

class WorkflowTemplate:
    """Base class for workflow templates."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.nodes: Dict[str, WorkflowNode] = {}
        self.metadata: Dict[str, Any] = {}
    
    def add_node(self, node: WorkflowNode) -> None:
        """Add a node to the workflow template."""
        self.nodes[node.id] = node
    
    def add_dependency(self, node_id: str, dependency_id: str) -> None:
        """Add a dependency between nodes."""
        if node_id in self.nodes:
            self.nodes[node_id].dependencies.append(dependency_id)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate the workflow template for cycles and consistency."""
        errors = []
        
        # Check for cycles
        try:
            graph = nx.DiGraph()
            for node_id, node in self.nodes.items():
                graph.add_node(node_id)
                for dep in node.dependencies:
                    graph.add_edge(dep, node_id)
            
            if not nx.is_directed_acyclic_graph(graph):
                errors.append("Workflow contains cycles")
        except Exception as e:
            errors.append(f"Graph validation error: {str(e)}")
        
        # Check dependencies exist
        for node_id, node in self.nodes.items():
            for dep in node.dependencies:
                if dep not in self.nodes:
                    errors.append(f"Node {node_id} depends on non-existent node {dep}")
        
        return len(errors) == 0, errors

class WorkflowOptimizer:
    """Optimizes workflow execution patterns for performance and resource efficiency."""
    
    def __init__(self):
        self.optimization_strategies = {
            'parallel_execution': self._optimize_parallel_execution,
            'resource_balancing': self._optimize_resource_balancing,
            'critical_path': self._optimize_critical_path,
            'load_distribution': self._optimize_load_distribution
        }
    
    def optimize_workflow(self, template: WorkflowTemplate, 
                         constraints: Dict[str, Any]) -> WorkflowTemplate:
        """Apply optimization strategies to a workflow template."""
        optimized = self._deep_copy_template(template)
        
        for strategy_name, strategy_func in self.optimization_strategies.items():
            if constraints.get(f'enable_{strategy_name}', True):
                optimized = strategy_func(optimized, constraints)
        
        return optimized
    
    def _optimize_parallel_execution(self, template: WorkflowTemplate, 
                                   constraints: Dict[str, Any]) -> WorkflowTemplate:
        """Identify and group tasks that can run in parallel."""
        graph = self._build_dependency_graph(template)
        parallel_groups = []
        
        # Find nodes with no dependencies that can run in parallel
        independent_nodes = [node_id for node_id, node in template.nodes.items() 
                           if not node.dependencies]
        
        if len(independent_nodes) > 1:
            group_id = str(uuid.uuid4())
            for node_id in independent_nodes:
                template.nodes[node_id].parallel_group = group_id
            parallel_groups.append(group_id)
        
        # Find other parallelizable groups using topological analysis
        try:
            levels = list(nx.topological_generations(graph))
            for level in levels:
                if len(level) > 1:
                    group_id = str(uuid.uuid4())
                    for node_id in level:
                        template.nodes[node_id].parallel_group = group_id
                    parallel_groups.append(group_id)
        except Exception as e:
            print(f"Parallel optimization warning: {e}")
        
        return template
    
    def _optimize_resource_balancing(self, template: WorkflowTemplate, 
                                   constraints: Dict[str, Any]) -> WorkflowTemplate:
        """Balance resource usage across workflow execution."""
        max_cpu = constraints.get('max_cpu_cores', 4)
        max_memory = constraints.get('max_memory_gb', 8)
        
        for node in template.nodes.values():
            # Set reasonable resource limits if not specified
            if 'cpu_cores' not in node.resource_requirements:
                node.resource_requirements['cpu_cores'] = min(1, max_cpu // 4)
            if 'memory_gb' not in node.resource_requirements:
                node.resource_requirements['memory_gb'] = min(1, max_memory // 4)
        
        return template
    
    def _optimize_critical_path(self, template: WorkflowTemplate, 
                              constraints: Dict[str, Any]) -> WorkflowTemplate:
        """Optimize the critical path for faster execution."""
        graph = self._build_dependency_graph(template)
        
        try:
            # Calculate critical path
            for node_id in nx.topological_sort(graph):
                node = template.nodes[node_id]
                if not node.dependencies:
                    node.priority = TaskPriority.HIGH
                else:
                    # Inherit highest priority from dependencies
                    dep_priorities = [template.nodes[dep].priority.value 
                                    for dep in node.dependencies]
                    if min(dep_priorities) <= TaskPriority.HIGH.value:
                        node.priority = TaskPriority.HIGH
        except Exception as e:
            print(f"Critical path optimization warning: {e}")
        
        return template
    
    def _optimize_load_distribution(self, template: WorkflowTemplate, 
                                  constraints: Dict[str, Any]) -> WorkflowTemplate:
        """Distribute load evenly across available resources."""
        total_nodes = len(template.nodes)
        max_concurrent = constraints.get('max_concurrent_tasks', 3)
        
        # Adjust timeouts based on load
        avg_timeout = sum(node.timeout for node in template.nodes.values()) / total_nodes
        for node in template.nodes.values():
            if total_nodes > max_concurrent:
                node.timeout = int(node.timeout * 1.5)  # Increase timeout for heavy loads
        
        return template
    
    def _build_dependency_graph(self, template: WorkflowTemplate) -> nx.DiGraph:
        """Build a NetworkX graph from the workflow template."""
        graph = nx.DiGraph()
        for node_id, node in template.nodes.items():
            graph.add_node(node_id, **node.__dict__)
            for dep in node.dependencies:
                graph.add_edge(dep, node_id)
        return graph
    
    def _deep_copy_template(self, template: WorkflowTemplate) -> WorkflowTemplate:
        """Create a deep copy of a workflow template."""
        new_template = WorkflowTemplate(template.name, template.description)
        new_template.metadata = template.metadata.copy()
        for node_id, node in template.nodes.items():
            new_node = WorkflowNode(
                id=node.id,
                name=node.name,
                task_type=node.task_type,
                agent_id=node.agent_id,
                dependencies=node.dependencies.copy(),
                parameters=node.parameters.copy(),
                priority=node.priority,
                estimated_duration=node.estimated_duration,
                timeout=node.timeout,
                retry_count=node.retry_count,
                conditions=node.conditions.copy(),
                parallel_group=node.parallel_group,
                resource_requirements=node.resource_requirements.copy()
            )
            new_template.add_node(new_node)
        return new_template

class WorkflowExecutor:
    """Executes workflows with advanced scheduling and monitoring."""
    
    def __init__(self, resource_manager=None, performance_monitor=None):
        self.resource_manager = resource_manager
        self.performance_monitor = performance_monitor
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.execution_queue: List[str] = []
        self.max_concurrent_executions = 5
    
    async def execute_workflow(self, template: WorkflowTemplate, 
                             context: Dict[str, Any] = None) -> WorkflowExecution:
        """Execute a workflow template with intelligent scheduling."""
        execution_id = str(uuid.uuid4())
        execution = WorkflowExecution(
            workflow_id=template.name,
            execution_id=execution_id,
            status=ExecutionStatus.PENDING,
            start_time=datetime.now(),
            context=context or {}
        )
        
        self.active_executions[execution_id] = execution
        
        try:
            execution.status = ExecutionStatus.RUNNING
            await self._execute_workflow_graph(template, execution)
            execution.status = ExecutionStatus.COMPLETED
        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.metrics['error'] = str(e)
            raise
        finally:
            execution.end_time = datetime.now()
            if execution.start_time:
                execution.metrics['total_duration'] = (
                    execution.end_time - execution.start_time
                ).total_seconds()
        
        return execution
    
    async def _execute_workflow_graph(self, template: WorkflowTemplate, 
                                    execution: WorkflowExecution) -> None:
        """Execute workflow nodes based on dependency graph."""
        graph = self._build_execution_graph(template)
        
        # Group nodes by parallel execution groups
        parallel_groups = self._group_parallel_nodes(template)
        
        for level_nodes in nx.topological_generations(graph):
            # Execute nodes in parallel groups
            level_tasks = []
            for node_id in level_nodes:
                if node_id not in execution.completed_nodes:
                    level_tasks.append(self._execute_node(template.nodes[node_id], execution))
            
            if level_tasks:
                await asyncio.gather(*level_tasks, return_exceptions=True)
    
    async def _execute_node(self, node: WorkflowNode, execution: WorkflowExecution) -> Any:
        """Execute a single workflow node."""
        start_time = datetime.now()
        execution.current_node = node.id
        execution.execution_path.append(node.id)
        
        try:
            # Check resource availability
            if self.resource_manager:
                await self.resource_manager.allocate_resources(node.resource_requirements)
            
            # Execute the actual task
            result = await self._execute_task(node, execution.context)
            
            execution.completed_nodes.add(node.id)
            end_time = datetime.now()
            execution.metrics[f'node_{node.id}_duration'] = (end_time - start_time).total_seconds()
            
            return result
            
        except Exception as e:
            execution.failed_nodes.add(node.id)
            execution.metrics[f'node_{node.id}_error'] = str(e)
            
            # Implement retry logic
            if node.retry_count > 0:
                node.retry_count -= 1
                await asyncio.sleep(1)  # Brief delay before retry
                return await self._execute_node(node, execution)
            else:
                raise
        finally:
            # Release resources
            if self.resource_manager:
                await self.resource_manager.release_resources(node.resource_requirements)
    
    async def _execute_task(self, node: WorkflowNode, context: Dict[str, Any]) -> Any:
        """Execute the actual task logic for a node."""
        # This would integrate with the actual agent execution system
        # For now, simulate task execution
        await asyncio.sleep(node.estimated_duration / 10)  # Simulated work
        
        return {
            'node_id': node.id,
            'task_type': node.task_type,
            'status': 'completed',
            'result': f'Task {node.name} completed successfully'
        }
    
    def _build_execution_graph(self, template: WorkflowTemplate) -> nx.DiGraph:
        """Build execution graph from template."""
        graph = nx.DiGraph()
        for node_id, node in template.nodes.items():
            graph.add_node(node_id)
            for dep in node.dependencies:
                graph.add_edge(dep, node_id)
        return graph
    
    def _group_parallel_nodes(self, template: WorkflowTemplate) -> Dict[str, List[str]]:
        """Group nodes that can execute in parallel."""
        groups = {}
        for node_id, node in template.nodes.items():
            if node.parallel_group:
                if node.parallel_group not in groups:
                    groups[node.parallel_group] = []
                groups[node.parallel_group].append(node_id)
        return groups

class WorkflowTemplateLibrary:
    """Library of pre-built workflow templates for common AI operations."""
    
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """Initialize common workflow templates."""
        
        # Data Processing Pipeline
        data_pipeline = WorkflowTemplate("data_processing_pipeline", 
                                        "Standard data ingestion and processing workflow")
        
        # Add nodes for data pipeline
        data_pipeline.add_node(WorkflowNode(
            id="data_ingestion",
            name="Data Ingestion",
            task_type="data_ingestion",
            priority=TaskPriority.HIGH,
            estimated_duration=120
        ))
        
        data_pipeline.add_node(WorkflowNode(
            id="data_validation",
            name="Data Validation",
            task_type="validation",
            dependencies=["data_ingestion"],
            priority=TaskPriority.HIGH,
            estimated_duration=60
        ))
        
        data_pipeline.add_node(WorkflowNode(
            id="data_transformation",
            name="Data Transformation",
            task_type="transformation",
            dependencies=["data_validation"],
            priority=TaskPriority.MEDIUM,
            estimated_duration=180
        ))
        
        data_pipeline.add_node(WorkflowNode(
            id="data_storage",
            name="Data Storage",
            task_type="storage",
            dependencies=["data_transformation"],
            priority=TaskPriority.MEDIUM,
            estimated_duration=90
        ))
        
        self.templates["data_processing_pipeline"] = data_pipeline
        
        # Multi-Agent Analysis Workflow
        analysis_workflow = WorkflowTemplate("multi_agent_analysis",
                                           "Collaborative analysis using multiple AI agents")
        
        analysis_workflow.add_node(WorkflowNode(
            id="requirements_analysis",
            name="Requirements Analysis",
            task_type="analysis",
            agent_id="analysis_agent",
            priority=TaskPriority.HIGH,
            estimated_duration=300
        ))
        
        analysis_workflow.add_node(WorkflowNode(
            id="security_review",
            name="Security Review",
            task_type="security_analysis",
            agent_id="security_agent",
            dependencies=["requirements_analysis"],
            priority=TaskPriority.CRITICAL,
            estimated_duration=240
        ))
        
        analysis_workflow.add_node(WorkflowNode(
            id="performance_analysis",
            name="Performance Analysis",
            task_type="performance_analysis",
            agent_id="performance_agent",
            dependencies=["requirements_analysis"],
            priority=TaskPriority.HIGH,
            estimated_duration=180
        ))
        
        analysis_workflow.add_node(WorkflowNode(
            id="compliance_check",
            name="Compliance Check",
            task_type="compliance_analysis",
            agent_id="compliance_agent",
            dependencies=["security_review", "performance_analysis"],
            priority=TaskPriority.HIGH,
            estimated_duration=120
        ))
        
        self.templates["multi_agent_analysis"] = analysis_workflow
    
    def get_template(self, template_name: str) -> Optional[WorkflowTemplate]:
        """Get a workflow template by name."""
        return self.templates.get(template_name)
    
    def list_templates(self) -> List[str]:
        """List all available template names."""
        return list(self.templates.keys())
    
    def add_template(self, template: WorkflowTemplate) -> None:
        """Add a new template to the library."""
        self.templates[template.name] = template

class AdaptiveWorkflowDesigner:
    """Advanced workflow designer with machine learning and adaptation capabilities."""
    
    def __init__(self):
        self.template_library = WorkflowTemplateLibrary()
        self.optimizer = WorkflowOptimizer()
        self.executor = WorkflowExecutor()
        self.execution_history: List[WorkflowExecution] = []
        self.performance_patterns: Dict[str, Any] = {}
    
    async def design_adaptive_workflow(self, requirements: Dict[str, Any], 
                                     constraints: Dict[str, Any] = None) -> WorkflowTemplate:
        """Design a workflow that adapts based on requirements and historical performance."""
        constraints = constraints or {}
        
        # Analyze requirements
        workflow_type = self._analyze_workflow_type(requirements)
        base_template = self._select_base_template(requirements, workflow_type)
        
        # Customize template based on requirements
        customized_template = self._customize_template(base_template, requirements)
        
        # Optimize based on constraints and historical data
        optimized_template = self.optimizer.optimize_workflow(customized_template, constraints)
        
        # Apply adaptive improvements based on execution history
        adaptive_template = self._apply_adaptive_improvements(optimized_template)
        
        return adaptive_template
    
    def _analyze_workflow_type(self, requirements: Dict[str, Any]) -> WorkflowType:
        """Analyze requirements to determine optimal workflow type."""
        complexity = requirements.get('complexity', 'medium')
        parallelizable = requirements.get('parallelizable', False)
        conditional_logic = requirements.get('has_conditions', False)
        
        if conditional_logic:
            return WorkflowType.CONDITIONAL
        elif parallelizable:
            return WorkflowType.PARALLEL
        elif complexity == 'high':
            return WorkflowType.HYBRID
        else:
            return WorkflowType.SEQUENTIAL
    
    def _select_base_template(self, requirements: Dict[str, Any], 
                            workflow_type: WorkflowType) -> WorkflowTemplate:
        """Select the most appropriate base template."""
        task_category = requirements.get('category', 'general')
        
        # Map categories to templates
        template_mapping = {
            'data_processing': 'data_processing_pipeline',
            'analysis': 'multi_agent_analysis',
            'general': 'data_processing_pipeline'  # Default
        }
        
        template_name = template_mapping.get(task_category, 'data_processing_pipeline')
        base_template = self.template_library.get_template(template_name)
        
        if not base_template:
            # Create a minimal template if none found
            base_template = WorkflowTemplate("custom_workflow", "Custom generated workflow")
            base_template.add_node(WorkflowNode(
                id="main_task",
                name="Main Task",
                task_type="general",
                priority=TaskPriority.MEDIUM
            ))
        
        return base_template
    
    def _customize_template(self, template: WorkflowTemplate, 
                          requirements: Dict[str, Any]) -> WorkflowTemplate:
        """Customize template based on specific requirements."""
        customized = self.optimizer._deep_copy_template(template)
        
        # Add custom nodes based on requirements
        custom_agents = requirements.get('agents', [])
        for agent_config in custom_agents:
            node = WorkflowNode(
                id=f"custom_{agent_config.get('id', str(uuid.uuid4()))}",
                name=agent_config.get('name', 'Custom Agent'),
                task_type=agent_config.get('type', 'general'),
                agent_id=agent_config.get('id'),
                priority=TaskPriority(agent_config.get('priority', 3)),
                estimated_duration=agent_config.get('duration', 120)
            )
            customized.add_node(node)
        
        return customized
    
    def _apply_adaptive_improvements(self, template: WorkflowTemplate) -> WorkflowTemplate:
        """Apply improvements based on execution history and patterns."""
        if not self.execution_history:
            return template
        
        # Analyze historical performance
        similar_executions = [
            exec for exec in self.execution_history 
            if exec.workflow_id == template.name
        ]
        
        if similar_executions:
            # Adjust timeouts based on historical data
            avg_durations = {}
            for execution in similar_executions:
                for metric_name, duration in execution.metrics.items():
                    if metric_name.endswith('_duration'):
                        node_id = metric_name.replace('node_', '').replace('_duration', '')
                        if node_id not in avg_durations:
                            avg_durations[node_id] = []
                        avg_durations[node_id].append(duration)
            
            # Update node estimates
            for node_id, durations in avg_durations.items():
                if node_id in template.nodes:
                    avg_duration = sum(durations) / len(durations)
                    template.nodes[node_id].estimated_duration = int(avg_duration * 1.2)  # Add buffer
                    template.nodes[node_id].timeout = int(avg_duration * 3)  # Conservative timeout
        
        return template
    
    async def execute_and_learn(self, template: WorkflowTemplate, 
                              context: Dict[str, Any] = None) -> WorkflowExecution:
        """Execute workflow and learn from the execution for future improvements."""
        execution = await self.executor.execute_workflow(template, context)
        
        # Store execution for learning
        self.execution_history.append(execution)
        
        # Update performance patterns
        self._update_performance_patterns(execution)
        
        # Limit history size
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-50:]
        
        return execution
    
    def _update_performance_patterns(self, execution: WorkflowExecution) -> None:
        """Update performance patterns based on execution results."""
        workflow_id = execution.workflow_id
        
        if workflow_id not in self.performance_patterns:
            self.performance_patterns[workflow_id] = {
                'avg_duration': 0,
                'success_rate': 0,
                'common_failures': {},
                'optimal_timeouts': {}
            }
        
        patterns = self.performance_patterns[workflow_id]
        
        # Update average duration
        if 'total_duration' in execution.metrics:
            current_avg = patterns['avg_duration']
            new_duration = execution.metrics['total_duration']
            patterns['avg_duration'] = (current_avg + new_duration) / 2
        
        # Update success rate
        if execution.status == ExecutionStatus.COMPLETED:
            patterns['success_rate'] = min(1.0, patterns['success_rate'] + 0.1)
        else:
            patterns['success_rate'] = max(0.0, patterns['success_rate'] - 0.1)
        
        # Track common failures
        if execution.failed_nodes:
            for node_id in execution.failed_nodes:
                if node_id not in patterns['common_failures']:
                    patterns['common_failures'][node_id] = 0
                patterns['common_failures'][node_id] += 1

def create_workflow_designer() -> AdaptiveWorkflowDesigner:
    """Factory function to create a configured workflow designer."""
    return AdaptiveWorkflowDesigner()
