"""
Advanced Architecture Optimizer for AI Orchestrator System
Handles intelligent system architecture optimization, pattern recognition, and adaptive improvements.
"""

import asyncio
import json
import networkx as nx
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import uuid
from collections import defaultdict, deque
from abc import ABC, abstractmethod
import math

class ArchitecturePattern(Enum):
    MICROSERVICES = "microservices"
    MONOLITH = "monolith"
    LAYERED = "layered"
    EVENT_DRIVEN = "event_driven"
    PIPELINE = "pipeline"
    MESH = "mesh"
    SERVERLESS = "serverless"
    HYBRID = "hybrid"

class OptimizationObjective(Enum):
    PERFORMANCE = "performance"
    SCALABILITY = "scalability"
    RELIABILITY = "reliability"
    MAINTAINABILITY = "maintainability"
    COST_EFFICIENCY = "cost_efficiency"
    SECURITY = "security"
    FLEXIBILITY = "flexibility"

class ComponentType(Enum):
    AGENT = "agent"
    SERVICE = "service"
    WORKFLOW = "workflow"
    DATA_STORE = "data_store"
    GATEWAY = "gateway"
    LOAD_BALANCER = "load_balancer"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"

@dataclass
class ArchitectureComponent:
    """Represents a component in the system architecture."""
    id: str
    name: str
    component_type: ComponentType
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    resource_usage: Dict[str, float] = field(default_factory=dict)
    configuration: Dict[str, Any] = field(default_factory=dict)
    health_score: float = 1.0
    last_updated: datetime = field(default_factory=datetime.now)
    tags: Set[str] = field(default_factory=set)

@dataclass
class ArchitectureMetrics:
    """Metrics for evaluating architecture quality."""
    performance_score: float = 0.0
    scalability_score: float = 0.0
    reliability_score: float = 0.0
    maintainability_score: float = 0.0
    security_score: float = 0.0
    cost_efficiency_score: float = 0.0
    overall_score: float = 0.0
    bottlenecks: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)

@dataclass
class OptimizationRecommendation:
    """Recommendation for architecture optimization."""
    id: str
    priority: int
    objective: OptimizationObjective
    description: str
    implementation_steps: List[str]
    estimated_impact: Dict[str, float]
    estimated_effort: int  # hours
    risk_level: float
    affected_components: List[str]
    prerequisites: List[str] = field(default_factory=list)

class ArchitectureAnalyzer:
    """Analyzes system architecture for patterns and optimization opportunities."""
    
    def __init__(self):
        self.analysis_cache: Dict[str, Any] = {}
        self.pattern_library = self._initialize_pattern_library()
        self.metrics_history: deque = deque(maxlen=1000)
    
    def _initialize_pattern_library(self) -> Dict[str, Dict[str, Any]]:
        """Initialize library of architecture patterns."""
        return {
            "microservices": {
                "characteristics": ["loose_coupling", "high_autonomy", "distributed"],
                "benefits": ["scalability", "flexibility", "fault_isolation"],
                "drawbacks": ["complexity", "network_overhead", "distributed_debugging"],
                "optimal_for": ["large_teams", "diverse_technologies", "independent_scaling"]
            },
            "monolith": {
                "characteristics": ["tight_coupling", "single_deployment", "centralized"],
                "benefits": ["simplicity", "performance", "easier_debugging"],
                "drawbacks": ["scaling_limitations", "technology_lock_in", "deployment_risk"],
                "optimal_for": ["small_teams", "simple_requirements", "rapid_prototyping"]
            },
            "event_driven": {
                "characteristics": ["asynchronous", "event_propagation", "loose_coupling"],
                "benefits": ["responsiveness", "scalability", "flexibility"],
                "drawbacks": ["complexity", "eventual_consistency", "debugging_difficulty"],
                "optimal_for": ["real_time_systems", "high_volume", "complex_workflows"]
            },
            "layered": {
                "characteristics": ["hierarchical", "abstraction_layers", "separation_of_concerns"],
                "benefits": ["maintainability", "testability", "clear_structure"],
                "drawbacks": ["performance_overhead", "rigidity", "layer_coupling"],
                "optimal_for": ["enterprise_applications", "clear_separation", "team_organization"]
            }
        }
    
    async def analyze_architecture(self, components: Dict[str, ArchitectureComponent]) -> ArchitectureMetrics:
        """Perform comprehensive architecture analysis."""
        metrics = ArchitectureMetrics()
        
        # Build dependency graph
        dependency_graph = self._build_dependency_graph(components)
        
        # Analyze different aspects
        metrics.performance_score = await self._analyze_performance(components, dependency_graph)
        metrics.scalability_score = await self._analyze_scalability(components, dependency_graph)
        metrics.reliability_score = await self._analyze_reliability(components, dependency_graph)
        metrics.maintainability_score = await self._analyze_maintainability(components, dependency_graph)
        metrics.security_score = await self._analyze_security(components, dependency_graph)
        metrics.cost_efficiency_score = await self._analyze_cost_efficiency(components)
        
        # Calculate overall score
        weights = {
            'performance': 0.25,
            'scalability': 0.20,
            'reliability': 0.20,
            'maintainability': 0.15,
            'security': 0.15,
            'cost_efficiency': 0.05
        }
        
        metrics.overall_score = (
            metrics.performance_score * weights['performance'] +
            metrics.scalability_score * weights['scalability'] +
            metrics.reliability_score * weights['reliability'] +
            metrics.maintainability_score * weights['maintainability'] +
            metrics.security_score * weights['security'] +
            metrics.cost_efficiency_score * weights['cost_efficiency']
        )
        
        # Identify bottlenecks
        metrics.bottlenecks = await self._identify_bottlenecks(components, dependency_graph)
        
        # Generate improvement suggestions
        metrics.improvement_suggestions = await self._generate_improvement_suggestions(
            components, dependency_graph, metrics
        )
        
        # Store metrics for historical analysis
        self.metrics_history.append((datetime.now(), metrics))
        
        return metrics
    
    def _build_dependency_graph(self, components: Dict[str, ArchitectureComponent]) -> nx.DiGraph:
        """Build a directed graph representing component dependencies."""
        graph = nx.DiGraph()
        
        for component_id, component in components.items():
            graph.add_node(component_id, component=component)
            
            for dependency_id in component.dependencies:
                if dependency_id in components:
                    graph.add_edge(dependency_id, component_id)
        
        return graph
    
    async def _analyze_performance(self, components: Dict[str, ArchitectureComponent], 
                                 graph: nx.DiGraph) -> float:
        """Analyze architecture performance characteristics."""
        performance_scores = []
        
        for component_id, component in components.items():
            # Component-level performance
            latency = component.performance_metrics.get('latency_ms', 100)
            throughput = component.performance_metrics.get('throughput_rps', 100)
            
            # Normalize scores (lower latency and higher throughput is better)
            latency_score = max(0, 1 - (latency / 1000))  # Normalize to 1000ms
            throughput_score = min(1, throughput / 1000)  # Normalize to 1000 RPS
            
            component_score = (latency_score + throughput_score) / 2
            performance_scores.append(component_score)
        
        # Consider path complexity (longer paths = potential performance issues)
        if len(components) > 1:
            try:
                avg_path_length = nx.average_shortest_path_length(graph.to_undirected())
                path_penalty = max(0, (avg_path_length - 2) * 0.1)  # Penalty for long paths
                base_score = sum(performance_scores) / len(performance_scores)
                return max(0, base_score - path_penalty)
            except (nx.NetworkXError, ZeroDivisionError):
                pass
        
        return sum(performance_scores) / len(performance_scores) if performance_scores else 0.5
    
    async def _analyze_scalability(self, components: Dict[str, ArchitectureComponent], 
                                 graph: nx.DiGraph) -> float:
        """Analyze architecture scalability characteristics."""
        scalability_factors = []
        
        # Analyze coupling (lower coupling = better scalability)
        coupling_score = self._calculate_coupling_score(graph)
        scalability_factors.append(coupling_score)
        
        # Analyze component autonomy
        autonomy_score = self._calculate_autonomy_score(components, graph)
        scalability_factors.append(autonomy_score)
        
        # Analyze resource distribution
        distribution_score = self._calculate_distribution_score(components)
        scalability_factors.append(distribution_score)
        
        # Analyze bottleneck potential
        bottleneck_score = await self._calculate_bottleneck_resilience(components, graph)
        scalability_factors.append(bottleneck_score)
        
        return sum(scalability_factors) / len(scalability_factors)
    
    async def _analyze_reliability(self, components: Dict[str, ArchitectureComponent], 
                                 graph: nx.DiGraph) -> float:
        """Analyze architecture reliability characteristics."""
        reliability_factors = []
        
        # Component health scores
        health_scores = [comp.health_score for comp in components.values()]
        avg_health = sum(health_scores) / len(health_scores) if health_scores else 0.5
        reliability_factors.append(avg_health)
        
        # Fault tolerance (redundancy and isolation)
        fault_tolerance_score = self._calculate_fault_tolerance(components, graph)
        reliability_factors.append(fault_tolerance_score)
        
        # Single points of failure
        spof_score = self._analyze_single_points_of_failure(graph)
        reliability_factors.append(spof_score)
        
        return sum(reliability_factors) / len(reliability_factors)
    
    async def _analyze_maintainability(self, components: Dict[str, ArchitectureComponent], 
                                     graph: nx.DiGraph) -> float:
        """Analyze architecture maintainability characteristics."""
        maintainability_factors = []
        
        # Component complexity
        complexity_score = self._calculate_complexity_score(components, graph)
        maintainability_factors.append(1 - complexity_score)  # Lower complexity = higher maintainability
        
        # Modularity
        modularity_score = self._calculate_modularity_score(graph)
        maintainability_factors.append(modularity_score)
        
        # Documentation and configuration clarity
        clarity_score = self._calculate_clarity_score(components)
        maintainability_factors.append(clarity_score)
        
        return sum(maintainability_factors) / len(maintainability_factors)
    
    async def _analyze_security(self, components: Dict[str, ArchitectureComponent], 
                              graph: nx.DiGraph) -> float:
        """Analyze architecture security characteristics."""
        security_factors = []
        
        # Attack surface analysis
        attack_surface_score = self._calculate_attack_surface_score(components, graph)
        security_factors.append(1 - attack_surface_score)  # Smaller surface = better security
        
        # Access control complexity
        access_control_score = self._calculate_access_control_score(components)
        security_factors.append(access_control_score)
        
        # Data flow security
        data_flow_score = self._calculate_data_flow_security(components, graph)
        security_factors.append(data_flow_score)
        
        return sum(security_factors) / len(security_factors)
    
    async def _analyze_cost_efficiency(self, components: Dict[str, ArchitectureComponent]) -> float:
        """Analyze architecture cost efficiency."""
        cost_factors = []
        
        # Resource utilization efficiency
        for component in components.values():
            cpu_util = component.resource_usage.get('cpu_utilization', 0.5)
            memory_util = component.resource_usage.get('memory_utilization', 0.5)
            
            # Optimal utilization is around 70-80%
            cpu_efficiency = 1 - abs(cpu_util - 0.75) / 0.75
            memory_efficiency = 1 - abs(memory_util - 0.75) / 0.75
            
            component_efficiency = (cpu_efficiency + memory_efficiency) / 2
            cost_factors.append(component_efficiency)
        
        return sum(cost_factors) / len(cost_factors) if cost_factors else 0.5
    
    def _calculate_coupling_score(self, graph: nx.DiGraph) -> float:
        """Calculate coupling score (lower is better for scalability)."""
        if graph.number_of_nodes() <= 1:
            return 1.0
        
        total_possible_edges = graph.number_of_nodes() * (graph.number_of_nodes() - 1)
        actual_edges = graph.number_of_edges()
        
        coupling_ratio = actual_edges / total_possible_edges if total_possible_edges > 0 else 0
        return max(0, 1 - coupling_ratio)  # Lower coupling = higher score
    
    def _calculate_autonomy_score(self, components: Dict[str, ArchitectureComponent], 
                                graph: nx.DiGraph) -> float:
        """Calculate component autonomy score."""
        autonomy_scores = []
        
        for component_id, component in components.items():
            # Components with fewer dependencies are more autonomous
            dependency_count = len(component.dependencies)
            dependent_count = len(component.dependents)
            
            # Normalize by total number of components
            total_components = len(components)
            dependency_ratio = dependency_count / max(total_components - 1, 1)
            dependent_ratio = dependent_count / max(total_components - 1, 1)
            
            autonomy = 1 - (dependency_ratio + dependent_ratio) / 2
            autonomy_scores.append(max(0, autonomy))
        
        return sum(autonomy_scores) / len(autonomy_scores) if autonomy_scores else 0.5
    
    def _calculate_distribution_score(self, components: Dict[str, ArchitectureComponent]) -> float:
        """Calculate resource distribution score."""
        if not components:
            return 0.5
        
        # Analyze resource usage distribution
        cpu_usages = [comp.resource_usage.get('cpu_utilization', 0.5) for comp in components.values()]
        memory_usages = [comp.resource_usage.get('memory_utilization', 0.5) for comp in components.values()]
        
        # Better distribution = lower variance
        cpu_variance = self._calculate_variance(cpu_usages)
        memory_variance = self._calculate_variance(memory_usages)
        
        # Convert variance to score (lower variance = higher score)
        cpu_score = max(0, 1 - cpu_variance * 4)  # Scale variance
        memory_score = max(0, 1 - memory_variance * 4)
        
        return (cpu_score + memory_score) / 2
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    async def _calculate_bottleneck_resilience(self, components: Dict[str, ArchitectureComponent], 
                                             graph: nx.DiGraph) -> float:
        """Calculate resilience to bottlenecks."""
        if graph.number_of_nodes() <= 1:
            return 1.0
        
        # Identify critical nodes (high betweenness centrality)
        try:
            centralities = nx.betweenness_centrality(graph)
            max_centrality = max(centralities.values()) if centralities else 0
            
            # Lower maximum centrality = better resilience
            resilience_score = max(0, 1 - max_centrality)
            return resilience_score
        except (nx.NetworkXError, ValueError):
            return 0.5
    
    def _calculate_fault_tolerance(self, components: Dict[str, ArchitectureComponent], 
                                 graph: nx.DiGraph) -> float:
        """Calculate fault tolerance score."""
        if graph.number_of_nodes() <= 1:
            return 1.0
        
        # Simulate node failures and measure connectivity
        connectivity_scores = []
        
        for node in graph.nodes():
            temp_graph = graph.copy()
            temp_graph.remove_node(node)
            
            # Check if graph remains connected
            if temp_graph.number_of_nodes() > 0:
                try:
                    is_connected = nx.is_weakly_connected(temp_graph)
                    connectivity_scores.append(1.0 if is_connected else 0.0)
                except nx.NetworkXError:
                    connectivity_scores.append(0.0)
        
        return sum(connectivity_scores) / len(connectivity_scores) if connectivity_scores else 0.5
    
    def _analyze_single_points_of_failure(self, graph: nx.DiGraph) -> float:
        """Analyze single points of failure."""
        if graph.number_of_nodes() <= 2:
            return 0.5  # Small graphs inherently have SPOFs
        
        # Find articulation points (cut vertices)
        try:
            undirected_graph = graph.to_undirected()
            articulation_points = list(nx.articulation_points(undirected_graph))
            spof_ratio = len(articulation_points) / graph.number_of_nodes()
            
            # Fewer SPOFs = higher score
            return max(0, 1 - spof_ratio)
        except nx.NetworkXError:
            return 0.5
    
    def _calculate_complexity_score(self, components: Dict[str, ArchitectureComponent], 
                                  graph: nx.DiGraph) -> float:
        """Calculate overall complexity score."""
        complexity_factors = []
        
        # Cyclomatic complexity (based on graph structure)
        edges = graph.number_of_edges()
        nodes = graph.number_of_nodes()
        connected_components = nx.number_weakly_connected_components(graph)
        
        if nodes > 0:
            cyclomatic = edges - nodes + connected_components
            normalized_cyclomatic = cyclomatic / max(nodes, 1)
            complexity_factors.append(min(1.0, normalized_cyclomatic))
        
        # Configuration complexity
        config_complexity = 0
        for component in components.values():
            config_size = len(component.configuration)
            config_complexity += min(1.0, config_size / 20)  # Normalize to 20 config items
        
        if components:
            complexity_factors.append(config_complexity / len(components))
        
        return sum(complexity_factors) / len(complexity_factors) if complexity_factors else 0.5
    
    def _calculate_modularity_score(self, graph: nx.DiGraph) -> float:
        """Calculate modularity score of the architecture."""
        if graph.number_of_nodes() <= 1:
            return 1.0
        
        try:
            # Convert to undirected for community detection
            undirected_graph = graph.to_undirected()
            
            # Simple modularity calculation based on clustering
            clustering_coeffs = nx.clustering(undirected_graph)
            avg_clustering = sum(clustering_coeffs.values()) / len(clustering_coeffs)
            
            return avg_clustering
        except (nx.NetworkXError, ZeroDivisionError):
            return 0.5
    
    def _calculate_clarity_score(self, components: Dict[str, ArchitectureComponent]) -> float:
        """Calculate clarity score based on documentation and naming."""
        clarity_scores = []
        
        for component in components.values():
            score = 0.0
            
            # Name clarity (length and descriptiveness)
            if component.name and len(component.name) > 3:
                score += 0.3
            
            # Configuration documentation
            if component.configuration:
                documented_configs = sum(1 for v in component.configuration.values() 
                                       if isinstance(v, str) and len(v) > 10)
                config_ratio = documented_configs / len(component.configuration)
                score += config_ratio * 0.4
            
            # Tags for categorization
            if component.tags:
                score += min(0.3, len(component.tags) * 0.1)
            
            clarity_scores.append(score)
        
        return sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0.5
    
    def _calculate_attack_surface_score(self, components: Dict[str, ArchitectureComponent], 
                                      graph: nx.DiGraph) -> float:
        """Calculate attack surface score."""
        # Simplified attack surface calculation
        external_facing_components = 0
        total_components = len(components)
        
        for component in components.values():
            # Components with no dependencies might be external-facing
            if not component.dependencies or 'external' in component.tags:
                external_facing_components += 1
        
        if total_components == 0:
            return 0.5
        
        attack_surface_ratio = external_facing_components / total_components
        return attack_surface_ratio  # Higher ratio = larger attack surface
    
    def _calculate_access_control_score(self, components: Dict[str, ArchitectureComponent]) -> float:
        """Calculate access control score."""
        access_scores = []
        
        for component in components.values():
            # Check for security-related configuration
            security_configs = [k for k in component.configuration.keys() 
                              if any(term in k.lower() for term in ['auth', 'security', 'access', 'permission'])]
            
            if component.configuration:
                security_ratio = len(security_configs) / len(component.configuration)
                access_scores.append(min(1.0, security_ratio * 3))  # Boost security configs
            else:
                access_scores.append(0.5)  # Default score for no config
        
        return sum(access_scores) / len(access_scores) if access_scores else 0.5
    
    def _calculate_data_flow_security(self, components: Dict[str, ArchitectureComponent], 
                                    graph: nx.DiGraph) -> float:
        """Calculate data flow security score."""
        # Simplified: fewer connections = better security isolation
        if graph.number_of_nodes() <= 1:
            return 1.0
        
        max_possible_connections = graph.number_of_nodes() * (graph.number_of_nodes() - 1)
        actual_connections = graph.number_of_edges()
        
        connection_ratio = actual_connections / max_possible_connections if max_possible_connections > 0 else 0
        isolation_score = max(0, 1 - connection_ratio)
        
        return isolation_score
    
    async def _identify_bottlenecks(self, components: Dict[str, ArchitectureComponent], 
                                  graph: nx.DiGraph) -> List[str]:
        """Identify potential bottlenecks in the architecture."""
        bottlenecks = []
        
        # High centrality nodes
        try:
            centralities = nx.betweenness_centrality(graph)
            threshold = 0.5
            for node_id, centrality in centralities.items():
                if centrality > threshold:
                    bottlenecks.append(f"High centrality component: {node_id}")
        except nx.NetworkXError:
            pass
        
        # Resource utilization bottlenecks
        for component_id, component in components.items():
            cpu_util = component.resource_usage.get('cpu_utilization', 0)
            memory_util = component.resource_usage.get('memory_utilization', 0)
            
            if cpu_util > 0.9:
                bottlenecks.append(f"High CPU utilization: {component_id}")
            if memory_util > 0.9:
                bottlenecks.append(f"High memory utilization: {component_id}")
        
        # Performance bottlenecks
        for component_id, component in components.items():
            latency = component.performance_metrics.get('latency_ms', 0)
            if latency > 500:  # 500ms threshold
                bottlenecks.append(f"High latency component: {component_id}")
        
        return bottlenecks
    
    async def _generate_improvement_suggestions(self, components: Dict[str, ArchitectureComponent], 
                                              graph: nx.DiGraph, 
                                              metrics: ArchitectureMetrics) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        # Performance improvements
        if metrics.performance_score < 0.7:
            suggestions.append("Consider implementing caching layers for frequently accessed data")
            suggestions.append("Optimize database queries and add appropriate indexes")
        
        # Scalability improvements
        if metrics.scalability_score < 0.7:
            suggestions.append("Consider breaking down monolithic components into microservices")
            suggestions.append("Implement horizontal scaling capabilities")
        
        # Reliability improvements
        if metrics.reliability_score < 0.7:
            suggestions.append("Add redundancy for critical components")
            suggestions.append("Implement circuit breakers and retry mechanisms")
        
        # Security improvements
        if metrics.security_score < 0.7:
            suggestions.append("Implement proper authentication and authorization")
            suggestions.append("Add encryption for data in transit and at rest")
        
        # Architecture-specific suggestions
        if graph.number_of_edges() > graph.number_of_nodes() * 1.5:
            suggestions.append("Reduce coupling between components")
        
        if len(metrics.bottlenecks) > 0:
            suggestions.append("Address identified bottlenecks to improve overall performance")
        
        return suggestions

class PatternDetector:
    """Detects architectural patterns in the current system."""
    
    def __init__(self, analyzer: ArchitectureAnalyzer):
        self.analyzer = analyzer
        self.pattern_signatures = self._initialize_pattern_signatures()
    
    def _initialize_pattern_signatures(self) -> Dict[str, Dict[str, Any]]:
        """Initialize pattern detection signatures."""
        return {
            "microservices": {
                "min_components": 3,
                "max_coupling": 0.3,
                "autonomy_threshold": 0.7,
                "size_variance_max": 0.4
            },
            "monolith": {
                "max_components": 3,
                "min_coupling": 0.8,
                "centralization_threshold": 0.8
            },
            "layered": {
                "layer_detection": True,
                "hierarchical_threshold": 0.6,
                "cross_layer_penalty": 0.3
            },
            "event_driven": {
                "async_indicators": ["queue", "event", "message"],
                "loose_coupling": 0.4,
                "hub_detection": True
            }
        }
    
    async def detect_patterns(self, components: Dict[str, ArchitectureComponent], 
                            graph: nx.DiGraph) -> Dict[str, float]:
        """Detect architectural patterns and return confidence scores."""
        pattern_scores = {}
        
        for pattern_name, signature in self.pattern_signatures.items():
            score = await self._evaluate_pattern_match(pattern_name, signature, components, graph)
            pattern_scores[pattern_name] = score
        
        return pattern_scores
    
    async def _evaluate_pattern_match(self, pattern_name: str, signature: Dict[str, Any],
                                    components: Dict[str, ArchitectureComponent], 
                                    graph: nx.DiGraph) -> float:
        """Evaluate how well the architecture matches a specific pattern."""
        if pattern_name == "microservices":
            return await self._evaluate_microservices_pattern(signature, components, graph)
        elif pattern_name == "monolith":
            return await self._evaluate_monolith_pattern(signature, components, graph)
        elif pattern_name == "layered":
            return await self._evaluate_layered_pattern(signature, components, graph)
        elif pattern_name == "event_driven":
            return await self._evaluate_event_driven_pattern(signature, components, graph)
        else:
            return 0.0
    
    async def _evaluate_microservices_pattern(self, signature: Dict[str, Any],
                                            components: Dict[str, ArchitectureComponent], 
                                            graph: nx.DiGraph) -> float:
        """Evaluate microservices pattern match."""
        score_factors = []
        
        # Component count check
        component_count = len(components)
        if component_count >= signature["min_components"]:
            score_factors.append(1.0)
        else:
            score_factors.append(component_count / signature["min_components"])
        
        # Coupling check
        coupling_score = self.analyzer._calculate_coupling_score(graph)
        if coupling_score >= (1 - signature["max_coupling"]):
            score_factors.append(1.0)
        else:
            score_factors.append(coupling_score / (1 - signature["max_coupling"]))
        
        # Autonomy check
        autonomy_score = self.analyzer._calculate_autonomy_score(components, graph)
        if autonomy_score >= signature["autonomy_threshold"]:
            score_factors.append(1.0)
        else:
            score_factors.append(autonomy_score / signature["autonomy_threshold"])
        
        return sum(score_factors) / len(score_factors)
    
    async def _evaluate_monolith_pattern(self, signature: Dict[str, Any],
                                       components: Dict[str, ArchitectureComponent], 
                                       graph: nx.DiGraph) -> float:
        """Evaluate monolith pattern match."""
        score_factors = []
        
        # Component count (fewer components for monolith)
        component_count = len(components)
        if component_count <= signature["max_components"]:
            score_factors.append(1.0)
        else:
            score_factors.append(signature["max_components"] / component_count)
        
        # High coupling expected in monolith
        coupling_score = 1 - self.analyzer._calculate_coupling_score(graph)  # Invert for monolith
        if coupling_score >= signature["min_coupling"]:
            score_factors.append(1.0)
        else:
            score_factors.append(coupling_score / signature["min_coupling"])
        
        return sum(score_factors) / len(score_factors)
    
    async def _evaluate_layered_pattern(self, signature: Dict[str, Any],
                                      components: Dict[str, ArchitectureComponent], 
                                      graph: nx.DiGraph) -> float:
        """Evaluate layered pattern match."""
        # Simplified layered detection based on hierarchy
        try:
            # Check if graph is roughly hierarchical (DAG)
            if nx.is_directed_acyclic_graph(graph):
                # Calculate "layerness" based on topological levels
                levels = list(nx.topological_generations(graph))
                if len(levels) >= 3:  # At least 3 layers
                    return min(1.0, len(levels) / 5)  # Normalize to 5 layers max
            return 0.3  # Some layered characteristics
        except nx.NetworkXError:
            return 0.0
    
    async def _evaluate_event_driven_pattern(self, signature: Dict[str, Any],
                                           components: Dict[str, ArchitectureComponent], 
                                           graph: nx.DiGraph) -> float:
        """Evaluate event-driven pattern match."""
        score_factors = []
        
        # Look for event-related components
        event_components = 0
        for component in components.values():
            component_indicators = [component.name.lower(), str(component.tags).lower()]
            if any(indicator in " ".join(component_indicators) 
                  for indicator in signature["async_indicators"]):
                event_components += 1
        
        if components:
            event_ratio = event_components / len(components)
            score_factors.append(min(1.0, event_ratio * 3))  # Boost event indicators
        
        # Check for hub-like patterns (message brokers)
        try:
            centralities = nx.betweenness_centrality(graph)
            max_centrality = max(centralities.values()) if centralities else 0
            if max_centrality > 0.5:  # Strong hub detected
                score_factors.append(1.0)
            else:
                score_factors.append(max_centrality * 2)
        except nx.NetworkXError:
            score_factors.append(0.5)
        
        return sum(score_factors) / len(score_factors) if score_factors else 0.0

class OptimizationEngine:
    """Engine for generating and prioritizing optimization recommendations."""
    
    def __init__(self, analyzer: ArchitectureAnalyzer, pattern_detector: PatternDetector):
        self.analyzer = analyzer
        self.pattern_detector = pattern_detector
        self.optimization_rules = self._initialize_optimization_rules()
    
    def _initialize_optimization_rules(self) -> Dict[str, callable]:
        """Initialize optimization rule set."""
        return {
            "performance": self._generate_performance_optimizations,
            "scalability": self._generate_scalability_optimizations,
            "reliability": self._generate_reliability_optimizations,
            "maintainability": self._generate_maintainability_optimizations,
            "security": self._generate_security_optimizations,
            "cost": self._generate_cost_optimizations
        }
    
    async def generate_optimizations(self, components: Dict[str, ArchitectureComponent],
                                   metrics: ArchitectureMetrics,
                                   objectives: List[OptimizationObjective]) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations based on objectives."""
        recommendations = []
        
        for objective in objectives:
            objective_name = objective.value
            if objective_name in self.optimization_rules:
                rule_func = self.optimization_rules[objective_name]
                objective_recommendations = await rule_func(components, metrics)
                recommendations.extend(objective_recommendations)
        
        # Prioritize and deduplicate recommendations
        prioritized_recommendations = await self._prioritize_recommendations(recommendations, metrics)
        
        return prioritized_recommendations
    
    async def _generate_performance_optimizations(self, components: Dict[str, ArchitectureComponent],
                                                metrics: ArchitectureMetrics) -> List[OptimizationRecommendation]:
        """Generate performance optimization recommendations."""
        recommendations = []
        
        if metrics.performance_score < 0.7:
            # Cache implementation
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=1,
                objective=OptimizationObjective.PERFORMANCE,
                description="Implement distributed caching layer",
                implementation_steps=[
                    "Identify frequently accessed data",
                    "Choose appropriate caching technology (Redis, Memcached)",
                    "Implement cache-aside pattern",
                    "Configure cache eviction policies",
                    "Monitor cache hit ratios"
                ],
                estimated_impact={"performance_score": 0.3, "latency_reduction": 0.4},
                estimated_effort=40,
                risk_level=0.3,
                affected_components=list(components.keys())
            ))
            
            # Database optimization
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=2,
                objective=OptimizationObjective.PERFORMANCE,
                description="Optimize database queries and indexing",
                implementation_steps=[
                    "Analyze slow query logs",
                    "Add missing database indexes",
                    "Optimize N+1 query problems",
                    "Implement query result caching",
                    "Consider read replicas for scaling"
                ],
                estimated_impact={"performance_score": 0.25, "database_response_time": 0.5},
                estimated_effort=24,
                risk_level=0.2,
                affected_components=[comp_id for comp_id, comp in components.items() 
                                   if comp.component_type == ComponentType.DATA_STORE]
            ))
        
        return recommendations
    
    async def _generate_scalability_optimizations(self, components: Dict[str, ArchitectureComponent],
                                                metrics: ArchitectureMetrics) -> List[OptimizationRecommendation]:
        """Generate scalability optimization recommendations."""
        recommendations = []
        
        if metrics.scalability_score < 0.7:
            # Microservices decomposition
            if len(components) <= 3:
                recommendations.append(OptimizationRecommendation(
                    id=str(uuid.uuid4()),
                    priority=1,
                    objective=OptimizationObjective.SCALABILITY,
                    description="Decompose monolithic components into microservices",
                    implementation_steps=[
                        "Identify service boundaries using domain-driven design",
                        "Extract independent business capabilities",
                        "Implement API contracts between services",
                        "Set up independent deployment pipelines",
                        "Implement distributed monitoring"
                    ],
                    estimated_impact={"scalability_score": 0.4, "deployment_flexibility": 0.6},
                    estimated_effort=120,
                    risk_level=0.7,
                    affected_components=list(components.keys())
                ))
            
            # Load balancing
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=2,
                objective=OptimizationObjective.SCALABILITY,
                description="Implement load balancing and auto-scaling",
                implementation_steps=[
                    "Deploy load balancer in front of services",
                    "Configure health checks",
                    "Implement horizontal pod autoscaling",
                    "Set up metrics-based scaling policies",
                    "Test scaling scenarios"
                ],
                estimated_impact={"scalability_score": 0.3, "capacity_utilization": 0.4},
                estimated_effort=32,
                risk_level=0.4,
                affected_components=[]
            ))
        
        return recommendations
    
    async def _generate_reliability_optimizations(self, components: Dict[str, ArchitectureComponent],
                                                metrics: ArchitectureMetrics) -> List[OptimizationRecommendation]:
        """Generate reliability optimization recommendations."""
        recommendations = []
        
        if metrics.reliability_score < 0.7:
            # Circuit breaker implementation
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=1,
                objective=OptimizationObjective.RELIABILITY,
                description="Implement circuit breaker pattern",
                implementation_steps=[
                    "Identify external service dependencies",
                    "Implement circuit breaker libraries",
                    "Configure failure thresholds",
                    "Add fallback mechanisms",
                    "Monitor circuit breaker states"
                ],
                estimated_impact={"reliability_score": 0.3, "failure_recovery_time": 0.5},
                estimated_effort=16,
                risk_level=0.2,
                affected_components=[comp_id for comp_id, comp in components.items() 
                                   if comp.dependencies]
            ))
            
            # Redundancy implementation
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=2,
                objective=OptimizationObjective.RELIABILITY,
                description="Add redundancy for critical components",
                implementation_steps=[
                    "Identify single points of failure",
                    "Deploy multiple instances of critical services",
                    "Implement data replication",
                    "Set up failover mechanisms",
                    "Test disaster recovery procedures"
                ],
                estimated_impact={"reliability_score": 0.4, "availability": 0.3},
                estimated_effort=60,
                risk_level=0.5,
                affected_components=[]
            ))
        
        return recommendations
    
    async def _generate_maintainability_optimizations(self, components: Dict[str, ArchitectureComponent],
                                                    metrics: ArchitectureMetrics) -> List[OptimizationRecommendation]:
        """Generate maintainability optimization recommendations."""
        recommendations = []
        
        if metrics.maintainability_score < 0.7:
            # Documentation improvement
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=3,
                objective=OptimizationObjective.MAINTAINABILITY,
                description="Improve system documentation and API specs",
                implementation_steps=[
                    "Create comprehensive API documentation",
                    "Document service dependencies",
                    "Add inline code documentation",
                    "Create deployment guides",
                    "Maintain architecture decision records"
                ],
                estimated_impact={"maintainability_score": 0.2, "onboarding_time": 0.4},
                estimated_effort=24,
                risk_level=0.1,
                affected_components=list(components.keys())
            ))
        
        return recommendations
    
    async def _generate_security_optimizations(self, components: Dict[str, ArchitectureComponent],
                                             metrics: ArchitectureMetrics) -> List[OptimizationRecommendation]:
        """Generate security optimization recommendations."""
        recommendations = []
        
        if metrics.security_score < 0.7:
            # Authentication/Authorization
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=1,
                objective=OptimizationObjective.SECURITY,
                description="Implement comprehensive authentication and authorization",
                implementation_steps=[
                    "Deploy identity provider (OAuth2/OpenID Connect)",
                    "Implement JWT token validation",
                    "Add role-based access control",
                    "Secure inter-service communication",
                    "Implement audit logging"
                ],
                estimated_impact={"security_score": 0.4, "compliance_score": 0.5},
                estimated_effort=48,
                risk_level=0.3,
                affected_components=list(components.keys())
            ))
        
        return recommendations
    
    async def _generate_cost_optimizations(self, components: Dict[str, ArchitectureComponent],
                                         metrics: ArchitectureMetrics) -> List[OptimizationRecommendation]:
        """Generate cost optimization recommendations."""
        recommendations = []
        
        if metrics.cost_efficiency_score < 0.7:
            # Resource optimization
            recommendations.append(OptimizationRecommendation(
                id=str(uuid.uuid4()),
                priority=3,
                objective=OptimizationObjective.COST_EFFICIENCY,
                description="Optimize resource allocation and utilization",
                implementation_steps=[
                    "Analyze resource usage patterns",
                    "Right-size compute instances",
                    "Implement auto-scaling policies",
                    "Use spot instances where appropriate",
                    "Optimize storage costs"
                ],
                estimated_impact={"cost_efficiency_score": 0.3, "infrastructure_cost": -0.25},
                estimated_effort=16,
                risk_level=0.2,
                affected_components=list(components.keys())
            ))
        
        return recommendations
    
    async def _prioritize_recommendations(self, recommendations: List[OptimizationRecommendation],
                                        metrics: ArchitectureMetrics) -> List[OptimizationRecommendation]:
        """Prioritize optimization recommendations."""
        # Score each recommendation
        for rec in recommendations:
            priority_score = (5 - rec.priority) * 0.3  # Lower priority number = higher score
            impact_score = sum(rec.estimated_impact.values()) * 0.4
            effort_score = max(0, (100 - rec.estimated_effort) / 100) * 0.2  # Less effort = higher score
            risk_score = (1 - rec.risk_level) * 0.1  # Lower risk = higher score
            
            rec.estimated_impact['priority_score'] = priority_score + impact_score + effort_score + risk_score
        
        # Sort by priority score
        recommendations.sort(key=lambda r: r.estimated_impact.get('priority_score', 0), reverse=True)
        
        return recommendations

class AdvancedArchitectureOptimizer:
    """Main architecture optimizer that coordinates all optimization activities."""
    
    def __init__(self):
        self.analyzer = ArchitectureAnalyzer()
        self.pattern_detector = PatternDetector(self.analyzer)
        self.optimization_engine = OptimizationEngine(self.analyzer, self.pattern_detector)
        self.components: Dict[str, ArchitectureComponent] = {}
        self.optimization_history: List[Dict[str, Any]] = []
    
    async def register_component(self, component: ArchitectureComponent) -> None:
        """Register a component in the architecture."""
        self.components[component.id] = component
        
        # Update dependent relationships
        for dep_id in component.dependencies:
            if dep_id in self.components:
                if component.id not in self.components[dep_id].dependents:
                    self.components[dep_id].dependents.append(component.id)
    
    async def update_component_metrics(self, component_id: str, 
                                     performance_metrics: Dict[str, float],
                                     resource_usage: Dict[str, float]) -> None:
        """Update component metrics."""
        if component_id in self.components:
            self.components[component_id].performance_metrics.update(performance_metrics)
            self.components[component_id].resource_usage.update(resource_usage)
            self.components[component_id].last_updated = datetime.now()
    
    async def optimize_architecture(self, objectives: List[OptimizationObjective]) -> Dict[str, Any]:
        """Perform comprehensive architecture optimization."""
        # Analyze current architecture
        metrics = await self.analyzer.analyze_architecture(self.components)
        
        # Detect architectural patterns
        dependency_graph = self.analyzer._build_dependency_graph(self.components)
        patterns = await self.pattern_detector.detect_patterns(self.components, dependency_graph)
        
        # Generate optimization recommendations
        recommendations = await self.optimization_engine.generate_optimizations(
            self.components, metrics, objectives
        )
        
        # Prepare optimization report
        optimization_report = {
            'timestamp': datetime.now().isoformat(),
            'current_metrics': {
                'performance_score': metrics.performance_score,
                'scalability_score': metrics.scalability_score,
                'reliability_score': metrics.reliability_score,
                'maintainability_score': metrics.maintainability_score,
                'security_score': metrics.security_score,
                'cost_efficiency_score': metrics.cost_efficiency_score,
                'overall_score': metrics.overall_score
            },
            'detected_patterns': patterns,
            'bottlenecks': metrics.bottlenecks,
            'recommendations': [
                {
                    'id': rec.id,
                    'priority': rec.priority,
                    'objective': rec.objective.value,
                    'description': rec.description,
                    'estimated_impact': rec.estimated_impact,
                    'estimated_effort': rec.estimated_effort,
                    'risk_level': rec.risk_level
                }
                for rec in recommendations
            ],
            'component_count': len(self.components),
            'architecture_complexity': self._calculate_architecture_complexity()
        }
        
        # Store in history
        self.optimization_history.append(optimization_report)
        
        return optimization_report
    
    def _calculate_architecture_complexity(self) -> float:
        """Calculate overall architecture complexity score."""
        if not self.components:
            return 0.0
        
        # Component count factor
        component_factor = min(1.0, len(self.components) / 20)  # Normalize to 20 components
        
        # Dependency complexity
        total_dependencies = sum(len(comp.dependencies) for comp in self.components.values())
        dependency_factor = min(1.0, total_dependencies / (len(self.components) * 3))  # Avg 3 deps per component
        
        # Configuration complexity
        config_items = sum(len(comp.configuration) for comp in self.components.values())
        config_factor = min(1.0, config_items / (len(self.components) * 10))  # Avg 10 configs per component
        
        return (component_factor + dependency_factor + config_factor) / 3
    
    async def get_optimization_insights(self) -> Dict[str, Any]:
        """Get insights from optimization history."""
        if not self.optimization_history:
            return {}
        
        # Analyze trends
        recent_reports = self.optimization_history[-10:]  # Last 10 reports
        
        metric_trends = {}
        for metric in ['performance_score', 'scalability_score', 'reliability_score']:
            values = [report['current_metrics'][metric] for report in recent_reports]
            if len(values) > 1:
                trend = 'improving' if values[-1] > values[0] else 'declining'
                metric_trends[metric] = {
                    'trend': trend,
                    'change': values[-1] - values[0]
                }
        
        return {
            'total_optimizations': len(self.optimization_history),
            'metric_trends': metric_trends,
            'last_optimization': self.optimization_history[-1]['timestamp'] if self.optimization_history else None
        }

def create_architecture_optimizer() -> AdvancedArchitectureOptimizer:
    """Factory function to create a configured architecture optimizer."""
    return AdvancedArchitectureOptimizer()
