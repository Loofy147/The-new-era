"""
Advanced Performance Analyzer for AI Orchestrator System
Handles intelligent performance monitoring, analysis, and optimization recommendations.
"""

import asyncio
import time
import statistics
from typing import Dict, List, Any, Optional, Tuple, Set, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import uuid
import json
from collections import defaultdict, deque
from abc import ABC, abstractmethod
import threading
import psutil

class PerformanceMetricType(Enum):
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    RESOURCE_UTILIZATION = "resource_utilization"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    NETWORK_IO = "network_io"
    DISK_IO = "disk_io"
    RESPONSE_TIME = "response_time"
    QUEUE_DEPTH = "queue_depth"
    CUSTOM = "custom"

class AlertSeverity(Enum):
    INFO = 1
    WARNING = 2
    CRITICAL = 3
    EMERGENCY = 4

class AnalysisType(Enum):
    REAL_TIME = "real_time"
    BATCH = "batch"
    TREND = "trend"
    ANOMALY = "anomaly"
    PREDICTIVE = "predictive"

@dataclass
class PerformanceMetric:
    """Represents a performance metric measurement."""
    name: str
    metric_type: PerformanceMetricType
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.now)
    source_component: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)
    threshold_info: Optional[Dict[str, float]] = None

@dataclass
class PerformanceAlert:
    """Represents a performance alert."""
    id: str
    severity: AlertSeverity
    metric_name: str
    current_value: float
    threshold_value: float
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    source_component: Optional[str] = None
    resolved: bool = False
    resolution_timestamp: Optional[datetime] = None

@dataclass
class PerformanceBaseline:
    """Represents performance baseline for comparison."""
    metric_name: str
    baseline_value: float
    confidence_interval: Tuple[float, float]
    sample_size: int
    calculation_date: datetime
    validity_period: timedelta = field(default=timedelta(days=7))

@dataclass
class PerformanceReport:
    """Comprehensive performance analysis report."""
    analysis_id: str
    analysis_type: AnalysisType
    time_range: Tuple[datetime, datetime]
    summary_metrics: Dict[str, float]
    detailed_metrics: List[PerformanceMetric]
    alerts: List[PerformanceAlert]
    bottlenecks: List[str]
    recommendations: List[str]
    trends: Dict[str, str]
    anomalies: List[Dict[str, Any]]
    performance_score: float
    generated_at: datetime = field(default_factory=datetime.now)

class MetricCollector:
    """Collects performance metrics from various sources."""
    
    def __init__(self, collection_interval: int = 10):
        self.collection_interval = collection_interval
        self.collectors: Dict[str, Callable] = {}
        self.collected_metrics: deque = deque(maxlen=10000)
        self.collecting = False
        self.collector_thread: Optional[threading.Thread] = None
        self.custom_metrics: Dict[str, Any] = {}
    
    def register_collector(self, name: str, collector_func: Callable) -> None:
        """Register a custom metric collector."""
        self.collectors[name] = collector_func
    
    def start_collection(self) -> None:
        """Start metric collection."""
        if not self.collecting:
            self.collecting = True
            self.collector_thread = threading.Thread(target=self._collection_loop, daemon=True)
            self.collector_thread.start()
    
    def stop_collection(self) -> None:
        """Stop metric collection."""
        self.collecting = False
        if self.collector_thread and self.collector_thread.is_alive():
            self.collector_thread.join(timeout=5)
    
    def _collection_loop(self) -> None:
        """Main collection loop."""
        while self.collecting:
            try:
                metrics = self._collect_all_metrics()
                for metric in metrics:
                    self.collected_metrics.append(metric)
                time.sleep(self.collection_interval)
            except Exception as e:
                print(f"Metric collection error: {e}")
    
    def _collect_all_metrics(self) -> List[PerformanceMetric]:
        """Collect all registered metrics."""
        metrics = []
        
        # System metrics
        metrics.extend(self._collect_system_metrics())
        
        # Custom collector metrics
        for collector_name, collector_func in self.collectors.items():
            try:
                custom_metrics = collector_func()
                if isinstance(custom_metrics, list):
                    metrics.extend(custom_metrics)
                elif isinstance(custom_metrics, PerformanceMetric):
                    metrics.append(custom_metrics)
            except Exception as e:
                print(f"Error in collector {collector_name}: {e}")
        
        return metrics
    
    def _collect_system_metrics(self) -> List[PerformanceMetric]:
        """Collect system performance metrics."""
        metrics = []
        current_time = datetime.now()
        
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            metrics.append(PerformanceMetric(
                name="system_cpu_usage",
                metric_type=PerformanceMetricType.CPU_USAGE,
                value=cpu_percent,
                unit="percent",
                timestamp=current_time,
                source_component="system"
            ))
            
            # Memory metrics
            memory = psutil.virtual_memory()
            metrics.append(PerformanceMetric(
                name="system_memory_usage",
                metric_type=PerformanceMetricType.MEMORY_USAGE,
                value=memory.percent,
                unit="percent",
                timestamp=current_time,
                source_component="system"
            ))
            
            # Disk I/O metrics
            disk_io = psutil.disk_io_counters()
            if disk_io:
                metrics.append(PerformanceMetric(
                    name="system_disk_read_bytes",
                    metric_type=PerformanceMetricType.DISK_IO,
                    value=disk_io.read_bytes,
                    unit="bytes",
                    timestamp=current_time,
                    source_component="system"
                ))
                
                metrics.append(PerformanceMetric(
                    name="system_disk_write_bytes",
                    metric_type=PerformanceMetricType.DISK_IO,
                    value=disk_io.write_bytes,
                    unit="bytes",
                    timestamp=current_time,
                    source_component="system"
                ))
            
            # Network I/O metrics
            network_io = psutil.net_io_counters()
            if network_io:
                metrics.append(PerformanceMetric(
                    name="system_network_sent_bytes",
                    metric_type=PerformanceMetricType.NETWORK_IO,
                    value=network_io.bytes_sent,
                    unit="bytes",
                    timestamp=current_time,
                    source_component="system"
                ))
                
                metrics.append(PerformanceMetric(
                    name="system_network_recv_bytes",
                    metric_type=PerformanceMetricType.NETWORK_IO,
                    value=network_io.bytes_recv,
                    unit="bytes",
                    timestamp=current_time,
                    source_component="system"
                ))
            
        except Exception as e:
            print(f"System metrics collection error: {e}")
        
        return metrics
    
    def get_recent_metrics(self, metric_name: Optional[str] = None, 
                          time_range: Optional[timedelta] = None) -> List[PerformanceMetric]:
        """Get recent metrics, optionally filtered."""
        if time_range is None:
            time_range = timedelta(minutes=30)
        
        cutoff_time = datetime.now() - time_range
        
        filtered_metrics = [
            metric for metric in self.collected_metrics
            if metric.timestamp >= cutoff_time
        ]
        
        if metric_name:
            filtered_metrics = [
                metric for metric in filtered_metrics
                if metric.name == metric_name
            ]
        
        return filtered_metrics
    
    def add_custom_metric(self, metric: PerformanceMetric) -> None:
        """Add a custom metric measurement."""
        self.collected_metrics.append(metric)

class ThresholdManager:
    """Manages performance thresholds and alert conditions."""
    
    def __init__(self):
        self.thresholds: Dict[str, Dict[str, float]] = {}
        self.dynamic_thresholds: Dict[str, Any] = {}
        self.alert_cooldowns: Dict[str, datetime] = {}
        self.cooldown_period = timedelta(minutes=5)
    
    def set_threshold(self, metric_name: str, warning_threshold: float, 
                     critical_threshold: float, threshold_type: str = "upper") -> None:
        """Set static thresholds for a metric."""
        self.thresholds[metric_name] = {
            "warning": warning_threshold,
            "critical": critical_threshold,
            "type": threshold_type  # "upper", "lower", or "range"
        }
    
    def set_dynamic_threshold(self, metric_name: str, baseline: PerformanceBaseline,
                            multiplier: float = 2.0) -> None:
        """Set dynamic threshold based on baseline."""
        self.dynamic_thresholds[metric_name] = {
            "baseline": baseline,
            "multiplier": multiplier
        }
    
    def check_thresholds(self, metric: PerformanceMetric) -> Optional[PerformanceAlert]:
        """Check if metric violates thresholds."""
        # Check cooldown
        if metric.name in self.alert_cooldowns:
            if datetime.now() - self.alert_cooldowns[metric.name] < self.cooldown_period:
                return None
        
        # Check static thresholds
        if metric.name in self.thresholds:
            threshold_config = self.thresholds[metric.name]
            alert = self._check_static_threshold(metric, threshold_config)
            if alert:
                self.alert_cooldowns[metric.name] = datetime.now()
                return alert
        
        # Check dynamic thresholds
        if metric.name in self.dynamic_thresholds:
            threshold_config = self.dynamic_thresholds[metric.name]
            alert = self._check_dynamic_threshold(metric, threshold_config)
            if alert:
                self.alert_cooldowns[metric.name] = datetime.now()
                return alert
        
        return None
    
    def _check_static_threshold(self, metric: PerformanceMetric, 
                              threshold_config: Dict[str, Any]) -> Optional[PerformanceAlert]:
        """Check static threshold violations."""
        threshold_type = threshold_config.get("type", "upper")
        warning_threshold = threshold_config["warning"]
        critical_threshold = threshold_config["critical"]
        
        if threshold_type == "upper":
            if metric.value >= critical_threshold:
                return self._create_alert(metric, AlertSeverity.CRITICAL, critical_threshold)
            elif metric.value >= warning_threshold:
                return self._create_alert(metric, AlertSeverity.WARNING, warning_threshold)
        elif threshold_type == "lower":
            if metric.value <= critical_threshold:
                return self._create_alert(metric, AlertSeverity.CRITICAL, critical_threshold)
            elif metric.value <= warning_threshold:
                return self._create_alert(metric, AlertSeverity.WARNING, warning_threshold)
        
        return None
    
    def _check_dynamic_threshold(self, metric: PerformanceMetric, 
                               threshold_config: Dict[str, Any]) -> Optional[PerformanceAlert]:
        """Check dynamic threshold violations."""
        baseline = threshold_config["baseline"]
        multiplier = threshold_config["multiplier"]
        
        # Check if baseline is still valid
        if datetime.now() - baseline.calculation_date > baseline.validity_period:
            return None
        
        upper_bound = baseline.confidence_interval[1] * multiplier
        lower_bound = baseline.confidence_interval[0] / multiplier
        
        if metric.value > upper_bound:
            return self._create_alert(metric, AlertSeverity.WARNING, upper_bound)
        elif metric.value < lower_bound:
            return self._create_alert(metric, AlertSeverity.WARNING, lower_bound)
        
        return None
    
    def _create_alert(self, metric: PerformanceMetric, severity: AlertSeverity, 
                     threshold_value: float) -> PerformanceAlert:
        """Create a performance alert."""
        return PerformanceAlert(
            id=str(uuid.uuid4()),
            severity=severity,
            metric_name=metric.name,
            current_value=metric.value,
            threshold_value=threshold_value,
            message=f"{metric.name} {severity.name.lower()}: {metric.value:.2f} {metric.unit} "
                   f"exceeds threshold {threshold_value:.2f} {metric.unit}",
            source_component=metric.source_component
        )

class BaselineCalculator:
    """Calculates performance baselines for metrics."""
    
    def __init__(self, min_samples: int = 100):
        self.min_samples = min_samples
        self.baselines: Dict[str, PerformanceBaseline] = {}
    
    async def calculate_baseline(self, metric_name: str, 
                               metrics: List[PerformanceMetric],
                               confidence_level: float = 0.95) -> Optional[PerformanceBaseline]:
        """Calculate baseline for a metric."""
        # Filter metrics for the specific metric name
        filtered_metrics = [m for m in metrics if m.name == metric_name]
        
        if len(filtered_metrics) < self.min_samples:
            return None
        
        values = [m.value for m in filtered_metrics]
        
        # Calculate statistical baseline
        mean_value = statistics.mean(values)
        std_dev = statistics.stdev(values) if len(values) > 1 else 0
        
        # Calculate confidence interval
        z_score = 1.96 if confidence_level == 0.95 else 2.58  # 95% or 99%
        margin = z_score * (std_dev / (len(values) ** 0.5))
        
        confidence_interval = (mean_value - margin, mean_value + margin)
        
        baseline = PerformanceBaseline(
            metric_name=metric_name,
            baseline_value=mean_value,
            confidence_interval=confidence_interval,
            sample_size=len(values),
            calculation_date=datetime.now()
        )
        
        self.baselines[metric_name] = baseline
        return baseline
    
    async def update_baselines(self, metrics: List[PerformanceMetric]) -> None:
        """Update all baselines with new metric data."""
        metric_groups = defaultdict(list)
        
        # Group metrics by name
        for metric in metrics:
            metric_groups[metric.name].append(metric)
        
        # Update baselines for each metric
        for metric_name, metric_list in metric_groups.items():
            if len(metric_list) >= self.min_samples:
                await self.calculate_baseline(metric_name, metric_list)
    
    def get_baseline(self, metric_name: str) -> Optional[PerformanceBaseline]:
        """Get baseline for a metric."""
        baseline = self.baselines.get(metric_name)
        
        # Check if baseline is still valid
        if baseline and datetime.now() - baseline.calculation_date <= baseline.validity_period:
            return baseline
        
        return None

class AnomalyDetector:
    """Detects anomalies in performance metrics."""
    
    def __init__(self, sensitivity: float = 2.0):
        self.sensitivity = sensitivity  # Standard deviations for anomaly detection
        self.metric_histories: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
    
    async def detect_anomalies(self, metrics: List[PerformanceMetric]) -> List[Dict[str, Any]]:
        """Detect anomalies in the provided metrics."""
        anomalies = []
        
        # Update histories
        for metric in metrics:
            self.metric_histories[metric.name].append(metric.value)
        
        # Detect anomalies for each metric
        for metric in metrics:
            if len(self.metric_histories[metric.name]) >= 30:  # Minimum history
                anomaly = await self._detect_metric_anomaly(metric)
                if anomaly:
                    anomalies.append(anomaly)
        
        return anomalies
    
    async def _detect_metric_anomaly(self, metric: PerformanceMetric) -> Optional[Dict[str, Any]]:
        """Detect anomaly for a specific metric."""
        history = list(self.metric_histories[metric.name])
        
        if len(history) < 30:
            return None
        
        # Use recent history excluding the current value
        recent_history = history[:-1]
        current_value = metric.value
        
        # Statistical anomaly detection
        mean_value = statistics.mean(recent_history)
        std_dev = statistics.stdev(recent_history) if len(recent_history) > 1 else 0
        
        if std_dev == 0:
            return None
        
        z_score = abs(current_value - mean_value) / std_dev
        
        if z_score > self.sensitivity:
            return {
                'metric_name': metric.name,
                'current_value': current_value,
                'expected_value': mean_value,
                'z_score': z_score,
                'deviation': abs(current_value - mean_value),
                'timestamp': metric.timestamp,
                'severity': 'high' if z_score > 3.0 else 'medium',
                'source_component': metric.source_component
            }
        
        return None

class TrendAnalyzer:
    """Analyzes performance trends over time."""
    
    def __init__(self):
        self.trend_cache: Dict[str, Dict[str, Any]] = {}
    
    async def analyze_trends(self, metrics: List[PerformanceMetric], 
                           time_window: timedelta = timedelta(hours=24)) -> Dict[str, str]:
        """Analyze trends for all metrics."""
        trends = {}
        
        # Group metrics by name
        metric_groups = defaultdict(list)
        cutoff_time = datetime.now() - time_window
        
        for metric in metrics:
            if metric.timestamp >= cutoff_time:
                metric_groups[metric.name].append(metric)
        
        # Analyze trend for each metric
        for metric_name, metric_list in metric_groups.items():
            if len(metric_list) >= 10:  # Minimum data points for trend analysis
                trend = await self._calculate_trend(metric_name, metric_list)
                trends[metric_name] = trend
        
        return trends
    
    async def _calculate_trend(self, metric_name: str, 
                             metrics: List[PerformanceMetric]) -> str:
        """Calculate trend for a specific metric."""
        # Sort by timestamp
        sorted_metrics = sorted(metrics, key=lambda m: m.timestamp)
        values = [m.value for m in sorted_metrics]
        
        if len(values) < 10:
            return "insufficient_data"
        
        # Simple linear regression slope
        n = len(values)
        x_values = list(range(n))
        
        # Calculate slope
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            return "stable"
        
        slope = numerator / denominator
        
        # Classify trend
        if abs(slope) < 0.01:
            return "stable"
        elif slope > 0.1:
            return "strongly_increasing"
        elif slope > 0.01:
            return "increasing"
        elif slope < -0.1:
            return "strongly_decreasing"
        else:
            return "decreasing"

class BottleneckAnalyzer:
    """Analyzes performance bottlenecks."""
    
    def __init__(self):
        self.bottleneck_patterns = {
            'cpu_bottleneck': {
                'indicators': ['high_cpu_usage', 'low_memory_usage'],
                'threshold': 0.8
            },
            'memory_bottleneck': {
                'indicators': ['high_memory_usage', 'frequent_gc'],
                'threshold': 0.9
            },
            'io_bottleneck': {
                'indicators': ['high_disk_io', 'high_queue_depth'],
                'threshold': 0.7
            },
            'network_bottleneck': {
                'indicators': ['high_network_io', 'packet_loss'],
                'threshold': 0.8
            }
        }
    
    async def analyze_bottlenecks(self, metrics: List[PerformanceMetric]) -> List[str]:
        """Analyze and identify performance bottlenecks."""
        bottlenecks = []
        
        # Group metrics by component
        component_metrics = defaultdict(list)
        for metric in metrics:
            if metric.source_component:
                component_metrics[metric.source_component].append(metric)
        
        # Analyze each component
        for component, comp_metrics in component_metrics.items():
            component_bottlenecks = await self._analyze_component_bottlenecks(component, comp_metrics)
            bottlenecks.extend(component_bottlenecks)
        
        # System-wide bottleneck analysis
        system_bottlenecks = await self._analyze_system_bottlenecks(metrics)
        bottlenecks.extend(system_bottlenecks)
        
        return bottlenecks
    
    async def _analyze_component_bottlenecks(self, component: str, 
                                           metrics: List[PerformanceMetric]) -> List[str]:
        """Analyze bottlenecks for a specific component."""
        bottlenecks = []
        
        # Create metric lookup
        metric_values = {metric.name: metric.value for metric in metrics}
        
        # Check CPU bottleneck
        cpu_usage = metric_values.get(f"{component}_cpu_usage", 0)
        if cpu_usage > 80:
            bottlenecks.append(f"CPU bottleneck in {component}")
        
        # Check memory bottleneck
        memory_usage = metric_values.get(f"{component}_memory_usage", 0)
        if memory_usage > 90:
            bottlenecks.append(f"Memory bottleneck in {component}")
        
        # Check response time bottleneck
        response_time = metric_values.get(f"{component}_response_time", 0)
        if response_time > 1000:  # 1 second
            bottlenecks.append(f"Response time bottleneck in {component}")
        
        return bottlenecks
    
    async def _analyze_system_bottlenecks(self, metrics: List[PerformanceMetric]) -> List[str]:
        """Analyze system-wide bottlenecks."""
        bottlenecks = []
        
        # Create metric lookup
        metric_values = {metric.name: metric.value for metric in metrics}
        
        # System CPU bottleneck
        system_cpu = metric_values.get("system_cpu_usage", 0)
        if system_cpu > 85:
            bottlenecks.append("System-wide CPU bottleneck")
        
        # System memory bottleneck
        system_memory = metric_values.get("system_memory_usage", 0)
        if system_memory > 90:
            bottlenecks.append("System-wide memory bottleneck")
        
        # Network bottleneck (simplified)
        network_sent = metric_values.get("system_network_sent_bytes", 0)
        network_recv = metric_values.get("system_network_recv_bytes", 0)
        if network_sent > 1000000000 or network_recv > 1000000000:  # 1GB
            bottlenecks.append("Network I/O bottleneck")
        
        return bottlenecks

class PerformancePredictor:
    """Predicts future performance based on historical data."""
    
    def __init__(self):
        self.prediction_models: Dict[str, Any] = {}
    
    async def predict_performance(self, metric_name: str, 
                                metrics: List[PerformanceMetric],
                                prediction_horizon: timedelta = timedelta(hours=1)) -> Dict[str, Any]:
        """Predict future performance for a metric."""
        # Filter metrics for the specific metric
        filtered_metrics = [m for m in metrics if m.name == metric_name]
        
        if len(filtered_metrics) < 20:
            return {
                'predicted_value': None,
                'confidence': 0.0,
                'trend': 'unknown',
                'reason': 'insufficient_data'
            }
        
        # Sort by timestamp
        sorted_metrics = sorted(filtered_metrics, key=lambda m: m.timestamp)
        values = [m.value for m in sorted_metrics]
        
        # Simple linear extrapolation
        return await self._linear_prediction(values, prediction_horizon)
    
    async def _linear_prediction(self, values: List[float], 
                               horizon: timedelta) -> Dict[str, Any]:
        """Perform linear prediction."""
        n = len(values)
        x_values = list(range(n))
        
        # Calculate linear regression
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        if denominator == 0:
            return {
                'predicted_value': y_mean,
                'confidence': 0.5,
                'trend': 'stable',
                'reason': 'no_variance'
            }
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Predict future value
        future_x = n + (horizon.total_seconds() / 60)  # Assuming 1-minute intervals
        predicted_value = slope * future_x + intercept
        
        # Calculate confidence based on R-squared
        y_pred = [slope * x + intercept for x in x_values]
        ss_res = sum((values[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((values[i] - y_mean) ** 2 for i in range(n))
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        confidence = max(0.1, min(0.9, r_squared))
        
        # Determine trend
        if abs(slope) < 0.01:
            trend = 'stable'
        elif slope > 0:
            trend = 'increasing'
        else:
            trend = 'decreasing'
        
        return {
            'predicted_value': predicted_value,
            'confidence': confidence,
            'trend': trend,
            'slope': slope
        }

class AdvancedPerformanceAnalyzer:
    """Main performance analyzer that coordinates all analysis activities."""
    
    def __init__(self, collection_interval: int = 10):
        self.metric_collector = MetricCollector(collection_interval)
        self.threshold_manager = ThresholdManager()
        self.baseline_calculator = BaselineCalculator()
        self.anomaly_detector = AnomalyDetector()
        self.trend_analyzer = TrendAnalyzer()
        self.bottleneck_analyzer = BottleneckAnalyzer()
        self.performance_predictor = PerformancePredictor()
        
        self.active_alerts: List[PerformanceAlert] = []
        self.analysis_history: List[PerformanceReport] = []
        self.auto_analysis_enabled = True
        self.analysis_interval = 300  # 5 minutes
        self._analysis_task: Optional[asyncio.Task] = None
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
    
    def _initialize_default_thresholds(self) -> None:
        """Initialize default performance thresholds."""
        # System thresholds
        self.threshold_manager.set_threshold("system_cpu_usage", 70.0, 90.0, "upper")
        self.threshold_manager.set_threshold("system_memory_usage", 80.0, 95.0, "upper")
        
        # Response time thresholds (in milliseconds)
        self.threshold_manager.set_threshold("response_time", 500.0, 2000.0, "upper")
        
        # Error rate thresholds (percentage)
        self.threshold_manager.set_threshold("error_rate", 1.0, 5.0, "upper")
    
    async def start_analysis(self) -> None:
        """Start performance analysis."""
        self.metric_collector.start_collection()
        
        if self.auto_analysis_enabled:
            self._analysis_task = asyncio.create_task(self._auto_analysis_loop())
    
    async def stop_analysis(self) -> None:
        """Stop performance analysis."""
        self.metric_collector.stop_collection()
        
        if self._analysis_task:
            self._analysis_task.cancel()
            try:
                await self._analysis_task
            except asyncio.CancelledError:
                pass
    
    async def _auto_analysis_loop(self) -> None:
        """Automatic analysis loop."""
        while True:
            try:
                await asyncio.sleep(self.analysis_interval)
                await self.perform_analysis(AnalysisType.REAL_TIME)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Auto-analysis error: {e}")
    
    async def perform_analysis(self, analysis_type: AnalysisType = AnalysisType.REAL_TIME,
                             time_range: Optional[Tuple[datetime, datetime]] = None) -> PerformanceReport:
        """Perform comprehensive performance analysis."""
        analysis_id = str(uuid.uuid4())
        
        if time_range is None:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)
            time_range = (start_time, end_time)
        
        # Get metrics for analysis
        metrics = self.metric_collector.get_recent_metrics(
            time_range=time_range[1] - time_range[0]
        )
        
        # Perform different types of analysis
        summary_metrics = await self._calculate_summary_metrics(metrics)
        alerts = await self._check_all_thresholds(metrics)
        bottlenecks = await self.bottleneck_analyzer.analyze_bottlenecks(metrics)
        trends = await self.trend_analyzer.analyze_trends(metrics)
        anomalies = await self.anomaly_detector.detect_anomalies(metrics)
        recommendations = await self._generate_recommendations(metrics, bottlenecks, anomalies)
        performance_score = await self._calculate_performance_score(summary_metrics, alerts, bottlenecks)
        
        # Create report
        report = PerformanceReport(
            analysis_id=analysis_id,
            analysis_type=analysis_type,
            time_range=time_range,
            summary_metrics=summary_metrics,
            detailed_metrics=metrics[-100:],  # Last 100 metrics
            alerts=alerts,
            bottlenecks=bottlenecks,
            recommendations=recommendations,
            trends=trends,
            anomalies=anomalies,
            performance_score=performance_score
        )
        
        # Store report
        self.analysis_history.append(report)
        
        # Limit history size
        if len(self.analysis_history) > 100:
            self.analysis_history = self.analysis_history[-50:]
        
        return report
    
    async def _calculate_summary_metrics(self, metrics: List[PerformanceMetric]) -> Dict[str, float]:
        """Calculate summary metrics from detailed metrics."""
        summary = {}
        
        # Group metrics by name
        metric_groups = defaultdict(list)
        for metric in metrics:
            metric_groups[metric.name].append(metric.value)
        
        # Calculate statistics for each metric
        for metric_name, values in metric_groups.items():
            if values:
                summary[f"{metric_name}_avg"] = statistics.mean(values)
                summary[f"{metric_name}_max"] = max(values)
                summary[f"{metric_name}_min"] = min(values)
                if len(values) > 1:
                    summary[f"{metric_name}_std"] = statistics.stdev(values)
        
        return summary
    
    async def _check_all_thresholds(self, metrics: List[PerformanceMetric]) -> List[PerformanceAlert]:
        """Check all metrics against thresholds."""
        new_alerts = []
        
        for metric in metrics:
            alert = self.threshold_manager.check_thresholds(metric)
            if alert:
                new_alerts.append(alert)
                self.active_alerts.append(alert)
        
        return new_alerts
    
    async def _generate_recommendations(self, metrics: List[PerformanceMetric],
                                      bottlenecks: List[str],
                                      anomalies: List[Dict[str, Any]]) -> List[str]:
        """Generate performance improvement recommendations."""
        recommendations = []
        
        # Bottleneck-based recommendations
        for bottleneck in bottlenecks:
            if "CPU bottleneck" in bottleneck:
                recommendations.append("Consider optimizing CPU-intensive operations or scaling horizontally")
            elif "Memory bottleneck" in bottleneck:
                recommendations.append("Review memory usage patterns and consider increasing available memory")
            elif "Response time bottleneck" in bottleneck:
                recommendations.append("Investigate slow operations and consider implementing caching")
        
        # Anomaly-based recommendations
        high_severity_anomalies = [a for a in anomalies if a.get('severity') == 'high']
        if high_severity_anomalies:
            recommendations.append("Investigate recent high-severity anomalies for potential issues")
        
        # Alert-based recommendations
        critical_alerts = [a for a in self.active_alerts if a.severity == AlertSeverity.CRITICAL]
        if critical_alerts:
            recommendations.append("Address critical performance alerts immediately")
        
        # General recommendations
        recent_metrics = metrics[-100:] if len(metrics) > 100 else metrics
        cpu_metrics = [m for m in recent_metrics if "cpu" in m.name.lower()]
        if cpu_metrics:
            avg_cpu = statistics.mean([m.value for m in cpu_metrics])
            if avg_cpu > 80:
                recommendations.append("High CPU usage detected - consider load balancing or optimization")
        
        return recommendations
    
    async def _calculate_performance_score(self, summary_metrics: Dict[str, float],
                                         alerts: List[PerformanceAlert],
                                         bottlenecks: List[str]) -> float:
        """Calculate overall performance score (0-100)."""
        base_score = 100.0
        
        # Deduct points for alerts
        for alert in alerts:
            if alert.severity == AlertSeverity.CRITICAL:
                base_score -= 20
            elif alert.severity == AlertSeverity.WARNING:
                base_score -= 10
        
        # Deduct points for bottlenecks
        base_score -= len(bottlenecks) * 5
        
        # Consider average metrics
        cpu_avg = summary_metrics.get("system_cpu_usage_avg", 50)
        memory_avg = summary_metrics.get("system_memory_usage_avg", 50)
        
        if cpu_avg > 80:
            base_score -= (cpu_avg - 80) * 0.5
        if memory_avg > 80:
            base_score -= (memory_avg - 80) * 0.5
        
        return max(0.0, min(100.0, base_score))
    
    def add_custom_metric(self, metric: PerformanceMetric) -> None:
        """Add a custom performance metric."""
        self.metric_collector.add_custom_metric(metric)
    
    def register_metric_collector(self, name: str, collector_func: Callable) -> None:
        """Register a custom metric collector."""
        self.metric_collector.register_collector(name, collector_func)
    
    def set_threshold(self, metric_name: str, warning_threshold: float, 
                     critical_threshold: float, threshold_type: str = "upper") -> None:
        """Set performance threshold for a metric."""
        self.threshold_manager.set_threshold(metric_name, warning_threshold, 
                                           critical_threshold, threshold_type)
    
    async def get_performance_insights(self) -> Dict[str, Any]:
        """Get insights from performance analysis history."""
        if not self.analysis_history:
            return {}
        
        recent_reports = self.analysis_history[-10:]  # Last 10 reports
        
        # Calculate trends
        performance_scores = [report.performance_score for report in recent_reports]
        alert_counts = [len(report.alerts) for report in recent_reports]
        
        insights = {
            'recent_performance_score': performance_scores[-1] if performance_scores else 0,
            'performance_trend': 'improving' if len(performance_scores) > 1 and 
                               performance_scores[-1] > performance_scores[0] else 'stable_or_declining',
            'average_alert_count': statistics.mean(alert_counts) if alert_counts else 0,
            'total_analyses': len(self.analysis_history),
            'active_alerts': len([a for a in self.active_alerts if not a.resolved])
        }
        
        return insights
    
    async def predict_performance(self, metric_name: str, 
                                prediction_horizon: timedelta = timedelta(hours=1)) -> Dict[str, Any]:
        """Predict future performance for a metric."""
        recent_metrics = self.metric_collector.get_recent_metrics(
            metric_name=metric_name,
            time_range=timedelta(hours=24)
        )
        
        return await self.performance_predictor.predict_performance(
            metric_name, recent_metrics, prediction_horizon
        )

def create_performance_analyzer(collection_interval: int = 10) -> AdvancedPerformanceAnalyzer:
    """Factory function to create a configured performance analyzer."""
    return AdvancedPerformanceAnalyzer(collection_interval)
