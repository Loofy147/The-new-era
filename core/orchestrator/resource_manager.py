"""
Advanced Resource Manager for AI Orchestrator System
Handles intelligent resource allocation, monitoring, and optimization across agents and workflows.
"""

import asyncio
import psutil
import threading
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import uuid
import json
from collections import defaultdict, deque
from abc import ABC, abstractmethod

class ResourceType(Enum):
    CPU = "cpu"
    MEMORY = "memory" 
    GPU = "gpu"
    DISK = "disk"
    NETWORK = "network"
    CUSTOM = "custom"

class ResourceState(Enum):
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    EXHAUSTED = "exhausted"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class AllocationPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    BACKGROUND = 5

@dataclass
class ResourceSpec:
    """Specification for a resource requirement or allocation."""
    resource_type: ResourceType
    amount: float
    unit: str
    priority: AllocationPriority = AllocationPriority.MEDIUM
    max_amount: Optional[float] = None
    min_amount: Optional[float] = None
    duration_estimate: Optional[int] = None  # seconds
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass
class ResourceAllocation:
    """Represents an active resource allocation."""
    allocation_id: str
    requester_id: str
    resource_spec: ResourceSpec
    allocated_amount: float
    allocation_time: datetime
    expected_release_time: Optional[datetime] = None
    actual_usage: float = 0.0
    efficiency_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResourcePool:
    """Represents a pool of resources of a specific type."""
    resource_type: ResourceType
    total_capacity: float
    available_capacity: float
    allocated_capacity: float
    reserved_capacity: float
    unit: str
    state: ResourceState = ResourceState.AVAILABLE
    allocations: Dict[str, ResourceAllocation] = field(default_factory=dict)
    utilization_history: deque = field(default_factory=lambda: deque(maxlen=100))
    metadata: Dict[str, Any] = field(default_factory=dict)

class ResourceMonitor:
    """Monitors system resources and provides real-time metrics."""
    
    def __init__(self, sampling_interval: int = 5):
        self.sampling_interval = sampling_interval
        self.monitoring = False
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.current_metrics: Dict[str, float] = {}
        self.monitor_thread: Optional[threading.Thread] = None
        self.callbacks: List[callable] = []
    
    def start_monitoring(self):
        """Start continuous resource monitoring."""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring."""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
    
    def add_callback(self, callback: callable):
        """Add a callback for resource metric updates."""
        self.callbacks.append(callback)
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                metrics = self._collect_system_metrics()
                self._update_metrics(metrics)
                self._notify_callbacks(metrics)
                threading.Event().wait(self.sampling_interval)
            except Exception as e:
                print(f"Resource monitoring error: {e}")
    
    def _collect_system_metrics(self) -> Dict[str, float]:
        """Collect current system resource metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free_gb = disk.free / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # Network metrics (basic)
            network = psutil.net_io_counters()
            network_sent_mb = network.bytes_sent / (1024**2)
            network_recv_mb = network.bytes_recv / (1024**2)
            
            return {
                'cpu_percent': cpu_percent,
                'cpu_cores': cpu_count,
                'memory_percent': memory_percent,
                'memory_available_gb': memory_available_gb,
                'memory_total_gb': memory_total_gb,
                'disk_percent': disk_percent,
                'disk_free_gb': disk_free_gb,
                'disk_total_gb': disk_total_gb,
                'network_sent_mb': network_sent_mb,
                'network_recv_mb': network_recv_mb,
                'timestamp': datetime.now().timestamp()
            }
        except Exception as e:
            print(f"Error collecting system metrics: {e}")
            return {}
    
    def _update_metrics(self, metrics: Dict[str, float]):
        """Update internal metrics storage."""
        self.current_metrics = metrics
        for metric_name, value in metrics.items():
            if metric_name != 'timestamp':
                self.metrics_history[metric_name].append((datetime.now(), value))
    
    def _notify_callbacks(self, metrics: Dict[str, float]):
        """Notify all registered callbacks of metric updates."""
        for callback in self.callbacks:
            try:
                callback(metrics)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def get_current_metrics(self) -> Dict[str, float]:
        """Get current resource metrics."""
        return self.current_metrics.copy()
    
    def get_metric_history(self, metric_name: str, duration_minutes: int = 60) -> List[Tuple[datetime, float]]:
        """Get historical data for a specific metric."""
        if metric_name not in self.metrics_history:
            return []
        
        cutoff_time = datetime.now() - timedelta(minutes=duration_minutes)
        return [(timestamp, value) for timestamp, value in self.metrics_history[metric_name] 
                if timestamp >= cutoff_time]

class ResourcePredictor:
    """Predicts future resource needs based on historical patterns."""
    
    def __init__(self, monitor: ResourceMonitor):
        self.monitor = monitor
        self.prediction_models: Dict[str, Any] = {}
        self.seasonal_patterns: Dict[str, List[float]] = {}
    
    def predict_resource_demand(self, resource_type: ResourceType, 
                              horizon_minutes: int = 30) -> Dict[str, float]:
        """Predict resource demand for the specified time horizon."""
        metric_name = f"{resource_type.value}_percent"
        history = self.monitor.get_metric_history(metric_name, duration_minutes=240)
        
        if len(history) < 10:
            # Not enough data for prediction
            current_metrics = self.monitor.get_current_metrics()
            return {
                'predicted_usage': current_metrics.get(metric_name, 50.0),
                'confidence': 0.3,
                'trend': 'stable'
            }
        
        # Simple trend analysis
        recent_values = [value for _, value in history[-20:]]
        older_values = [value for _, value in history[-40:-20]] if len(history) >= 40 else recent_values
        
        recent_avg = sum(recent_values) / len(recent_values)
        older_avg = sum(older_values) / len(older_values)
        
        trend_direction = "increasing" if recent_avg > older_avg else "decreasing"
        trend_magnitude = abs(recent_avg - older_avg)
        
        # Simple linear extrapolation
        if len(recent_values) >= 5:
            slope = (recent_values[-1] - recent_values[0]) / len(recent_values)
            predicted_usage = recent_values[-1] + (slope * horizon_minutes / 5)
        else:
            predicted_usage = recent_avg
        
        # Bound predictions to reasonable ranges
        predicted_usage = max(0, min(100, predicted_usage))
        
        confidence = max(0.4, min(0.9, 1.0 - (trend_magnitude / 50)))
        
        return {
            'predicted_usage': predicted_usage,
            'confidence': confidence,
            'trend': trend_direction,
            'trend_magnitude': trend_magnitude
        }
    
    def detect_anomalies(self, resource_type: ResourceType) -> List[Dict[str, Any]]:
        """Detect anomalous resource usage patterns."""
        metric_name = f"{resource_type.value}_percent"
        history = self.monitor.get_metric_history(metric_name, duration_minutes=120)
        
        if len(history) < 20:
            return []
        
        values = [value for _, value in history]
        timestamps = [timestamp for timestamp, _ in history]
        
        # Calculate statistical thresholds
        mean_value = sum(values) / len(values)
        variance = sum((x - mean_value) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        anomalies = []
        threshold = 2.5 * std_dev  # 2.5 sigma threshold
        
        for i, (timestamp, value) in enumerate(history):
            if abs(value - mean_value) > threshold:
                anomalies.append({
                    'timestamp': timestamp,
                    'value': value,
                    'expected_value': mean_value,
                    'deviation': abs(value - mean_value),
                    'severity': 'high' if abs(value - mean_value) > 3 * std_dev else 'medium'
                })
        
        return anomalies

class ResourceAllocator:
    """Handles intelligent resource allocation with priority management."""
    
    def __init__(self, monitor: ResourceMonitor, predictor: ResourcePredictor):
        self.monitor = monitor
        self.predictor = predictor
        self.resource_pools: Dict[ResourceType, ResourcePool] = {}
        self.allocation_queue: List[Tuple[str, ResourceSpec]] = []
        self.allocation_history: List[ResourceAllocation] = []
        self.allocation_strategies = {
            'first_fit': self._first_fit_allocation,
            'best_fit': self._best_fit_allocation,
            'priority_based': self._priority_based_allocation,
            'predictive': self._predictive_allocation
        }
        self._initialize_resource_pools()
    
    def _initialize_resource_pools(self):
        """Initialize resource pools based on system capabilities."""
        metrics = self.monitor.get_current_metrics()
        
        # CPU pool
        cpu_cores = metrics.get('cpu_cores', 4)
        self.resource_pools[ResourceType.CPU] = ResourcePool(
            resource_type=ResourceType.CPU,
            total_capacity=cpu_cores,
            available_capacity=cpu_cores,
            allocated_capacity=0.0,
            reserved_capacity=cpu_cores * 0.1,  # Reserve 10% for system
            unit="cores"
        )
        
        # Memory pool
        memory_total_gb = metrics.get('memory_total_gb', 8)
        self.resource_pools[ResourceType.MEMORY] = ResourcePool(
            resource_type=ResourceType.MEMORY,
            total_capacity=memory_total_gb,
            available_capacity=memory_total_gb * 0.8,  # Leave 20% for system
            allocated_capacity=0.0,
            reserved_capacity=memory_total_gb * 0.2,
            unit="GB"
        )
        
        # Disk pool
        disk_total_gb = metrics.get('disk_total_gb', 100)
        self.resource_pools[ResourceType.DISK] = ResourcePool(
            resource_type=ResourceType.DISK,
            total_capacity=disk_total_gb,
            available_capacity=disk_total_gb * 0.9,  # Leave 10% free
            allocated_capacity=0.0,
            reserved_capacity=disk_total_gb * 0.1,
            unit="GB"
        )
    
    async def allocate_resources(self, requester_id: str, 
                               resource_specs: List[ResourceSpec],
                               strategy: str = 'priority_based') -> Dict[str, str]:
        """Allocate resources based on specifications and strategy."""
        allocation_ids = {}
        
        for spec in resource_specs:
            if strategy in self.allocation_strategies:
                allocation_id = await self.allocation_strategies[strategy](requester_id, spec)
                if allocation_id:
                    allocation_ids[spec.resource_type.value] = allocation_id
                else:
                    # Allocation failed, clean up any successful allocations
                    for allocated_id in allocation_ids.values():
                        await self.release_resources(allocated_id)
                    raise ResourceAllocationError(f"Failed to allocate {spec.resource_type.value}")
            else:
                raise ValueError(f"Unknown allocation strategy: {strategy}")
        
        return allocation_ids
    
    async def _priority_based_allocation(self, requester_id: str, 
                                       spec: ResourceSpec) -> Optional[str]:
        """Allocate resources based on priority and availability."""
        pool = self.resource_pools.get(spec.resource_type)
        if not pool:
            return None
        
        # Check if we have enough available capacity
        required_amount = spec.amount
        if pool.available_capacity >= required_amount:
            # Direct allocation
            allocation_id = str(uuid.uuid4())
            allocation = ResourceAllocation(
                allocation_id=allocation_id,
                requester_id=requester_id,
                resource_spec=spec,
                allocated_amount=required_amount,
                allocation_time=datetime.now(),
                expected_release_time=datetime.now() + timedelta(
                    seconds=spec.duration_estimate or 300
                )
            )
            
            # Update pool state
            pool.available_capacity -= required_amount
            pool.allocated_capacity += required_amount
            pool.allocations[allocation_id] = allocation
            
            self.allocation_history.append(allocation)
            return allocation_id
        
        # Check if we can preempt lower priority allocations
        if spec.priority.value <= 2:  # Critical or High priority
            preemptable_amount = sum(
                alloc.allocated_amount for alloc in pool.allocations.values()
                if alloc.resource_spec.priority.value > spec.priority.value
            )
            
            if preemptable_amount >= required_amount:
                # Preempt lower priority allocations
                await self._preempt_allocations(pool, required_amount, spec.priority)
                return await self._priority_based_allocation(requester_id, spec)
        
        return None
    
    async def _predictive_allocation(self, requester_id: str, 
                                   spec: ResourceSpec) -> Optional[str]:
        """Allocate resources based on predictive analysis."""
        prediction = self.predictor.predict_resource_demand(
            spec.resource_type, 
            horizon_minutes=30
        )
        
        # If we predict high usage, be more conservative
        if prediction['predicted_usage'] > 80 and prediction['confidence'] > 0.7:
            # Reduce allocation or defer to lower priority
            if spec.priority.value > 2:  # Medium, Low, or Background
                return None  # Defer allocation
        
        # Otherwise, use priority-based allocation
        return await self._priority_based_allocation(requester_id, spec)
    
    async def _first_fit_allocation(self, requester_id: str, 
                                  spec: ResourceSpec) -> Optional[str]:
        """Simple first-fit allocation strategy."""
        return await self._priority_based_allocation(requester_id, spec)
    
    async def _best_fit_allocation(self, requester_id: str, 
                                 spec: ResourceSpec) -> Optional[str]:
        """Best-fit allocation to minimize fragmentation."""
        return await self._priority_based_allocation(requester_id, spec)
    
    async def _preempt_allocations(self, pool: ResourcePool, 
                                 required_amount: float,
                                 priority: AllocationPriority) -> None:
        """Preempt lower priority allocations to free up resources."""
        preemptable_allocations = [
            (allocation_id, allocation) for allocation_id, allocation in pool.allocations.items()
            if allocation.resource_spec.priority.value > priority.value
        ]
        
        # Sort by priority (lowest priority first)
        preemptable_allocations.sort(key=lambda x: x[1].resource_spec.priority.value, reverse=True)
        
        freed_amount = 0.0
        for allocation_id, allocation in preemptable_allocations:
            if freed_amount >= required_amount:
                break
            
            await self.release_resources(allocation_id)
            freed_amount += allocation.allocated_amount
    
    async def release_resources(self, allocation_id: str) -> bool:
        """Release a resource allocation."""
        for pool in self.resource_pools.values():
            if allocation_id in pool.allocations:
                allocation = pool.allocations[allocation_id]
                
                # Update pool state
                pool.available_capacity += allocation.allocated_amount
                pool.allocated_capacity -= allocation.allocated_amount
                
                # Calculate efficiency score
                if allocation.actual_usage > 0:
                    allocation.efficiency_score = min(1.0, allocation.actual_usage / allocation.allocated_amount)
                
                # Remove allocation
                del pool.allocations[allocation_id]
                return True
        
        return False
    
    def get_resource_utilization(self) -> Dict[str, Dict[str, float]]:
        """Get current resource utilization across all pools."""
        utilization = {}
        
        for resource_type, pool in self.resource_pools.items():
            utilization[resource_type.value] = {
                'total_capacity': pool.total_capacity,
                'available_capacity': pool.available_capacity,
                'allocated_capacity': pool.allocated_capacity,
                'utilization_percent': (pool.allocated_capacity / pool.total_capacity) * 100,
                'active_allocations': len(pool.allocations)
            }
        
        return utilization
    
    def get_allocation_efficiency(self) -> Dict[str, float]:
        """Calculate allocation efficiency metrics."""
        if not self.allocation_history:
            return {}
        
        efficiency_by_type = defaultdict(list)
        
        for allocation in self.allocation_history:
            if allocation.efficiency_score > 0:
                resource_type = allocation.resource_spec.resource_type.value
                efficiency_by_type[resource_type].append(allocation.efficiency_score)
        
        return {
            resource_type: sum(scores) / len(scores)
            for resource_type, scores in efficiency_by_type.items()
        }

class ResourceOptimizer:
    """Optimizes resource allocation patterns and suggests improvements."""
    
    def __init__(self, allocator: ResourceAllocator, monitor: ResourceMonitor):
        self.allocator = allocator
        self.monitor = monitor
        self.optimization_rules = {
            'consolidation': self._suggest_consolidation,
            'load_balancing': self._suggest_load_balancing,
            'preemption_tuning': self._suggest_preemption_tuning,
            'capacity_planning': self._suggest_capacity_planning
        }
    
    def analyze_and_optimize(self) -> Dict[str, List[str]]:
        """Analyze current state and suggest optimizations."""
        suggestions = {}
        
        for rule_name, rule_func in self.optimization_rules.items():
            try:
                rule_suggestions = rule_func()
                if rule_suggestions:
                    suggestions[rule_name] = rule_suggestions
            except Exception as e:
                print(f"Optimization rule {rule_name} failed: {e}")
        
        return suggestions
    
    def _suggest_consolidation(self) -> List[str]:
        """Suggest consolidation opportunities."""
        suggestions = []
        utilization = self.allocator.get_resource_utilization()
        
        for resource_type, metrics in utilization.items():
            if metrics['utilization_percent'] < 30 and metrics['active_allocations'] > 1:
                suggestions.append(
                    f"Consider consolidating {resource_type} allocations "
                    f"(current utilization: {metrics['utilization_percent']:.1f}%)"
                )
        
        return suggestions
    
    def _suggest_load_balancing(self) -> List[str]:
        """Suggest load balancing improvements."""
        suggestions = []
        
        # Analyze allocation patterns
        for pool in self.allocator.resource_pools.values():
            if pool.allocated_capacity / pool.total_capacity > 0.8:
                suggestions.append(
                    f"High {pool.resource_type.value} utilization detected "
                    f"({pool.allocated_capacity/pool.total_capacity*100:.1f}%). "
                    f"Consider distributing load or increasing capacity."
                )
        
        return suggestions
    
    def _suggest_preemption_tuning(self) -> List[str]:
        """Suggest preemption policy adjustments."""
        suggestions = []
        
        # Analyze preemption frequency
        recent_allocations = [
            alloc for alloc in self.allocator.allocation_history[-50:]
            if alloc.allocation_time > datetime.now() - timedelta(hours=1)
        ]
        
        high_priority_count = sum(
            1 for alloc in recent_allocations 
            if alloc.resource_spec.priority.value <= 2
        )
        
        if high_priority_count / max(len(recent_allocations), 1) > 0.7:
            suggestions.append(
                "High frequency of critical/high priority allocations detected. "
                "Consider reviewing priority assignments or increasing capacity."
            )
        
        return suggestions
    
    def _suggest_capacity_planning(self) -> List[str]:
        """Suggest capacity planning improvements."""
        suggestions = []
        
        # Analyze resource trends
        for resource_type in self.allocator.resource_pools.keys():
            prediction = self.allocator.predictor.predict_resource_demand(resource_type)
            
            if prediction['predicted_usage'] > 85 and prediction['confidence'] > 0.7:
                suggestions.append(
                    f"Predicted high {resource_type.value} usage "
                    f"({prediction['predicted_usage']:.1f}%). "
                    f"Consider scaling up capacity."
                )
        
        return suggestions

class ResourceAllocationError(Exception):
    """Exception raised when resource allocation fails."""
    pass

class AdvancedResourceManager:
    """Main resource manager that coordinates all resource management activities."""
    
    def __init__(self, sampling_interval: int = 5):
        self.monitor = ResourceMonitor(sampling_interval)
        self.predictor = ResourcePredictor(self.monitor)
        self.allocator = ResourceAllocator(self.monitor, self.predictor)
        self.optimizer = ResourceOptimizer(self.allocator, self.monitor)
        self.auto_optimization_enabled = True
        self.optimization_interval = 300  # 5 minutes
        self._optimization_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the resource manager."""
        self.monitor.start_monitoring()
        
        if self.auto_optimization_enabled:
            self._optimization_task = asyncio.create_task(self._auto_optimization_loop())
    
    async def stop(self):
        """Stop the resource manager."""
        self.monitor.stop_monitoring()
        
        if self._optimization_task:
            self._optimization_task.cancel()
            try:
                await self._optimization_task
            except asyncio.CancelledError:
                pass
    
    async def _auto_optimization_loop(self):
        """Automatic optimization loop."""
        while True:
            try:
                await asyncio.sleep(self.optimization_interval)
                suggestions = self.optimizer.analyze_and_optimize()
                if suggestions:
                    print(f"Resource optimization suggestions: {suggestions}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Auto-optimization error: {e}")
    
    async def allocate_resources(self, requester_id: str, 
                               requirements: Dict[str, Any]) -> Dict[str, str]:
        """High-level resource allocation interface."""
        resource_specs = self._parse_requirements(requirements)
        return await self.allocator.allocate_resources(requester_id, resource_specs)
    
    async def release_resources(self, allocation_ids: Dict[str, str]) -> bool:
        """Release multiple resource allocations."""
        success = True
        for allocation_id in allocation_ids.values():
            if not await self.allocator.release_resources(allocation_id):
                success = False
        return success
    
    def _parse_requirements(self, requirements: Dict[str, Any]) -> List[ResourceSpec]:
        """Parse resource requirements into ResourceSpec objects."""
        specs = []
        
        for resource_type_str, config in requirements.items():
            try:
                resource_type = ResourceType(resource_type_str)
                if isinstance(config, (int, float)):
                    # Simple amount specification
                    spec = ResourceSpec(
                        resource_type=resource_type,
                        amount=float(config),
                        unit=self._get_default_unit(resource_type)
                    )
                elif isinstance(config, dict):
                    # Detailed specification
                    spec = ResourceSpec(
                        resource_type=resource_type,
                        amount=config.get('amount', 1.0),
                        unit=config.get('unit', self._get_default_unit(resource_type)),
                        priority=AllocationPriority(config.get('priority', 3)),
                        max_amount=config.get('max_amount'),
                        min_amount=config.get('min_amount'),
                        duration_estimate=config.get('duration_estimate')
                    )
                else:
                    continue
                
                specs.append(spec)
            except (ValueError, KeyError) as e:
                print(f"Invalid resource requirement: {resource_type_str}: {e}")
        
        return specs
    
    def _get_default_unit(self, resource_type: ResourceType) -> str:
        """Get default unit for a resource type."""
        defaults = {
            ResourceType.CPU: "cores",
            ResourceType.MEMORY: "GB",
            ResourceType.GPU: "cards",
            ResourceType.DISK: "GB",
            ResourceType.NETWORK: "Mbps"
        }
        return defaults.get(resource_type, "units")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'current_metrics': self.monitor.get_current_metrics(),
            'resource_utilization': self.allocator.get_resource_utilization(),
            'allocation_efficiency': self.allocator.get_allocation_efficiency(),
            'optimization_suggestions': self.optimizer.analyze_and_optimize(),
            'active_allocations': sum(
                len(pool.allocations) for pool in self.allocator.resource_pools.values()
            )
        }

def create_resource_manager(sampling_interval: int = 5) -> AdvancedResourceManager:
    """Factory function to create a configured resource manager."""
    return AdvancedResourceManager(sampling_interval)
