"""
Shared utilities for AI Operating System Framework
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfigManager:
    """Centralized configuration management"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
        self.save_config()

class ReportManager:
    """Manages report generation and storage"""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def save_report(self, agent_name: str, report_data: Dict[str, Any]) -> str:
        """Save agent report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{agent_name.lower()}_report_{timestamp}.json"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Add metadata
        report_data.update({
            "generated_by": agent_name,
            "generated_at": datetime.now().isoformat(),
            "report_version": "1.0"
        })
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Report saved: {filepath}")
        return filepath
    
    def get_reports(self, agent_name: Optional[str] = None) -> List[str]:
        """Get list of available reports"""
        reports = []
        for filename in os.listdir(self.reports_dir):
            if filename.endswith('.json'):
                if agent_name is None or filename.startswith(agent_name.lower()):
                    reports.append(os.path.join(self.reports_dir, filename))
        return sorted(reports)
    
    def load_report(self, filepath: str) -> Dict[str, Any]:
        """Load report from file"""
        with open(filepath, 'r') as f:
            return json.load(f)

class MetricsCollector:
    """Collects and manages system metrics"""
    
    def __init__(self):
        self.metrics = {}
    
    def record_metric(self, agent_name: str, metric_name: str, value: Any) -> None:
        """Record a metric value"""
        if agent_name not in self.metrics:
            self.metrics[agent_name] = {}
        
        self.metrics[agent_name][metric_name] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_metrics(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get metrics for agent or all agents"""
        if agent_name:
            return self.metrics.get(agent_name, {})
        return self.metrics
    
    def export_metrics(self, filepath: str) -> None:
        """Export metrics to file"""
        with open(filepath, 'w') as f:
            json.dump(self.metrics, f, indent=2)

class SystemHealth:
    """System health monitoring utilities"""
    
    @staticmethod
    def check_disk_space(path: str = ".") -> Dict[str, Any]:
        """Check available disk space"""
        stat = os.statvfs(path)
        free_bytes = stat.f_bavail * stat.f_frsize
        total_bytes = stat.f_blocks * stat.f_frsize
        used_bytes = total_bytes - free_bytes
        
        return {
            "free_gb": free_bytes / (1024**3),
            "total_gb": total_bytes / (1024**3),
            "used_gb": used_bytes / (1024**3),
            "usage_percent": (used_bytes / total_bytes) * 100
        }
    
    @staticmethod
    def check_memory_usage() -> Dict[str, Any]:
        """Check memory usage (simplified)"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                "total_gb": memory.total / (1024**3),
                "available_gb": memory.available / (1024**3),
                "used_gb": memory.used / (1024**3),
                "usage_percent": memory.percent
            }
        except ImportError:
            return {"error": "psutil not available"}
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get basic system information"""
        import platform
        
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "hostname": platform.node()
        }

class EventBus:
    """Simple event bus for agent communication"""
    
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type: str, callback) -> None:
        """Subscribe to an event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def publish(self, event_type: str, data: Any) -> None:
        """Publish an event"""
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in event callback: {e}")
    
    def unsubscribe(self, event_type: str, callback) -> None:
        """Unsubscribe from an event type"""
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
            except ValueError:
                pass

class FileUtils:
    """File system utilities"""
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """Ensure directory exists"""
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def clean_old_files(directory: str, days: int = 30) -> int:
        """Clean files older than specified days"""
        import time
        
        if not os.path.exists(directory):
            return 0
        
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        cleaned_count = 0
        
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and os.path.getmtime(filepath) < cutoff_time:
                os.remove(filepath)
                cleaned_count += 1
        
        return cleaned_count
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """Get file size in bytes"""
        return os.path.getsize(filepath) if os.path.exists(filepath) else 0

class DataFormatter:
    """Data formatting utilities"""
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Format bytes to human readable string"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration to human readable string"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
    
    @staticmethod
    def truncate_string(text: str, max_length: int = 100) -> str:
        """Truncate string to maximum length"""
        return text[:max_length] + "..." if len(text) > max_length else text

# Global instances
config_manager = ConfigManager()
report_manager = ReportManager()
metrics_collector = MetricsCollector()
event_bus = EventBus()

# Export commonly used functions
__all__ = [
    'ConfigManager', 'ReportManager', 'MetricsCollector', 'SystemHealth',
    'EventBus', 'FileUtils', 'DataFormatter',
    'config_manager', 'report_manager', 'metrics_collector', 'event_bus'
]
