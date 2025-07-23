"""
AI Orchestrator System Package
Advanced intelligence coordination and system optimization
"""

from .ai_orchestrator_architect import create_orchestrator
from .workflow_designer import create_workflow_designer
from .resource_manager import create_resource_manager
from .decision_engine import create_decision_engine
from .architecture_optimizer import create_architecture_optimizer
from .performance_analyzer import create_performance_analyzer
from .intelligence_coordinator import create_intelligence_coordinator

__all__ = [
    'create_orchestrator',
    'create_workflow_designer', 
    'create_resource_manager',
    'create_decision_engine',
    'create_architecture_optimizer',
    'create_performance_analyzer',
    'create_intelligence_coordinator'
]

__version__ = '1.0.0'
__author__ = 'AI Operating System Team'
__description__ = 'Advanced AI orchestration and intelligence coordination system'
