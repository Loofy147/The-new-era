#!/usr/bin/env python3
"""
AI Operating System - Dataset Generator
Generates comprehensive JSONL datasets for agent training and LLM fine-tuning
"""

import json
import uuid
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import itertools

class DatasetGenerator:
    def __init__(self, output_dir: str = "datasets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Agent configurations
        self.agents = {
            "CostOptBot": {
                "role": "Cost Optimization & Analysis",
                "description": "Analyzes infrastructure costs and identifies potential savings",
                "capabilities": ["cost_analysis", "resource_optimization", "budget_forecasting"],
                "domains": ["cloud_infrastructure", "database_optimization", "container_scaling"]
            },
            "SecuBot": {
                "role": "Security Hardening & Monitoring", 
                "description": "Performs security scans and identifies vulnerabilities",
                "capabilities": ["vulnerability_scanning", "threat_detection", "compliance_checking"],
                "domains": ["network_security", "application_security", "data_protection"]
            },
            "ComplianceBot": {
                "role": "Regulatory Compliance Auditing",
                "description": "Ensures adherence to regulatory standards and frameworks",
                "capabilities": ["compliance_auditing", "policy_validation", "risk_assessment"],
                "domains": ["gdpr", "sox", "hipaa", "pci_dss"]
            },
            "TestGenie": {
                "role": "Automated Testing & QA",
                "description": "Performs comprehensive software testing and quality assurance",
                "capabilities": ["automated_testing", "performance_testing", "regression_testing"],
                "domains": ["unit_testing", "integration_testing", "load_testing"]
            },
            "PrivacyGuard": {
                "role": "Data Privacy & Protection",
                "description": "Monitors and protects sensitive data across systems",
                "capabilities": ["data_classification", "privacy_monitoring", "anonymization"],
                "domains": ["data_governance", "privacy_compliance", "data_retention"]
            },
            "InsightsBot": {
                "role": "Analytics & Business Intelligence",
                "description": "Generates insights from data and system metrics",
                "capabilities": ["data_analysis", "trend_identification", "predictive_analytics"],
                "domains": ["business_intelligence", "system_analytics", "performance_metrics"]
            },
            "ConvDesignBot": {
                "role": "Conversation Design & UX",
                "description": "Designs and optimizes conversational interfaces",
                "capabilities": ["conversation_design", "ux_optimization", "user_journey_mapping"],
                "domains": ["chatbot_design", "voice_interfaces", "user_experience"]
            },
            "ModelRefactor": {
                "role": "Code Refactoring & Optimization",
                "description": "Analyzes and improves code quality and structure",
                "capabilities": ["code_analysis", "refactoring", "optimization"],
                "domains": ["code_quality", "performance_optimization", "architecture_improvement"]
            },
            "ArchitectureBot": {
                "role": "System Architecture Design",
                "description": "Designs and validates system architectures",
                "capabilities": ["architecture_design", "system_validation", "scalability_analysis"],
                "domains": ["microservices", "cloud_architecture", "distributed_systems"]
            }
        }
        
        # System metrics templates
        self.metric_templates = [
            "cpu_usage", "memory_usage", "disk_usage", "network_io",
            "response_time", "throughput", "error_rate", "availability"
        ]
        
        # Common tasks and scenarios
        self.task_scenarios = [
            "cost_optimization", "security_audit", "compliance_check",
            "performance_analysis", "data_migration", "system_upgrade",
            "incident_response", "capacity_planning", "risk_assessment"
        ]

    def generate_agent_training_data(self, num_samples: int = 1000) -> List[Dict]:
        """Generate training data for agent behavior and responses"""
        
        training_data = []
        
        for _ in range(num_samples):
            agent_name = random.choice(list(self.agents.keys()))
            agent_config = self.agents[agent_name]
            
            # Generate conversation context
            context = self._generate_agent_context(agent_name, agent_config)
            
            # Generate input/output pairs
            sample = {
                "id": str(uuid.uuid4()),
                "timestamp": self._random_timestamp().isoformat(),
                "agent": agent_name,
                "role": agent_config["role"],
                "context": context,
                "input": self._generate_agent_input(agent_name, agent_config),
                "output": self._generate_agent_output(agent_name, agent_config),
                "metadata": {
                    "capabilities": agent_config["capabilities"],
                    "domains": agent_config["domains"],
                    "confidence": random.uniform(0.7, 0.99),
                    "execution_time_ms": random.randint(500, 5000)
                }
            }
            
            training_data.append(sample)
        
        return training_data

    def generate_system_interaction_data(self, num_samples: int = 500) -> List[Dict]:
        """Generate data for system-level interactions and orchestration"""
        
        interaction_data = []
        
        for _ in range(num_samples):
            # Multi-agent interaction scenarios
            involved_agents = random.sample(list(self.agents.keys()), random.randint(2, 4))
            scenario = random.choice(self.task_scenarios)
            
            sample = {
                "id": str(uuid.uuid4()),
                "timestamp": self._random_timestamp().isoformat(),
                "scenario": scenario,
                "involved_agents": involved_agents,
                "orchestration": self._generate_orchestration_plan(involved_agents, scenario),
                "execution_flow": self._generate_execution_flow(involved_agents),
                "dependencies": self._generate_dependencies(involved_agents),
                "expected_outcomes": self._generate_expected_outcomes(scenario),
                "coordination_messages": self._generate_coordination_messages(involved_agents),
                "metadata": {
                    "complexity": self._calculate_complexity(involved_agents, scenario),
                    "estimated_duration": random.randint(30, 300),
                    "resource_requirements": self._generate_resource_requirements()
                }
            }
            
            interaction_data.append(sample)
        
        return interaction_data

    def generate_monitoring_data(self, num_samples: int = 2000) -> List[Dict]:
        """Generate system monitoring and metrics data"""
        
        monitoring_data = []
        base_time = datetime.now() - timedelta(days=30)
        
        for i in range(num_samples):
            timestamp = base_time + timedelta(minutes=i * 15)  # 15-minute intervals
            
            sample = {
                "id": str(uuid.uuid4()),
                "timestamp": timestamp.isoformat(),
                "system_metrics": self._generate_system_metrics(),
                "agent_metrics": self._generate_agent_metrics(),
                "performance_indicators": self._generate_performance_indicators(),
                "health_score": self._calculate_health_score(),
                "alerts": self._generate_alerts(),
                "trends": self._generate_trends(),
                "anomalies": self._detect_anomalies(),
                "metadata": {
                    "collection_method": "automated",
                    "data_quality": random.uniform(0.8, 1.0),
                    "completeness": random.uniform(0.9, 1.0)
                }
            }
            
            monitoring_data.append(sample)
        
        return monitoring_data

    def generate_conversation_data(self, num_samples: int = 800) -> List[Dict]:
        """Generate conversation data for human-AI interaction training"""
        
        conversation_data = []
        
        conversation_types = [
            "task_assignment", "status_inquiry", "troubleshooting",
            "configuration", "analysis_request", "reporting"
        ]
        
        for _ in range(num_samples):
            conv_type = random.choice(conversation_types)
            
            sample = {
                "id": str(uuid.uuid4()),
                "timestamp": self._random_timestamp().isoformat(),
                "conversation_type": conv_type,
                "human_input": self._generate_human_input(conv_type),
                "ai_response": self._generate_ai_response(conv_type),
                "context": self._generate_conversation_context(conv_type),
                "intent": self._extract_intent(conv_type),
                "entities": self._extract_entities(conv_type),
                "sentiment": self._analyze_sentiment(),
                "follow_up_actions": self._generate_follow_up_actions(conv_type),
                "metadata": {
                    "user_satisfaction": random.uniform(0.6, 0.95),
                    "response_relevance": random.uniform(0.7, 0.98),
                    "task_completion": random.choice([True, False])
                }
            }
            
            conversation_data.append(sample)
        
        return conversation_data

    def generate_execution_logs(self, num_samples: int = 1500) -> List[Dict]:
        """Generate detailed execution logs for analysis and debugging"""
        
        execution_logs = []
        
        for _ in range(num_samples):
            agent_name = random.choice(list(self.agents.keys()))
            status = random.choices(
                ["success", "failed", "timeout", "error"],
                weights=[0.7, 0.15, 0.1, 0.05]
            )[0]
            
            start_time = self._random_timestamp()
            duration = random.randint(500, 30000)  # milliseconds
            
            sample = {
                "id": str(uuid.uuid4()),
                "execution_id": str(uuid.uuid4()),
                "agent_name": agent_name,
                "agent_version": f"v{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
                "start_time": start_time.isoformat(),
                "end_time": (start_time + timedelta(milliseconds=duration)).isoformat(),
                "duration_ms": duration,
                "status": status,
                "input_parameters": self._generate_input_parameters(agent_name),
                "output_data": self._generate_output_data(agent_name, status),
                "error_details": self._generate_error_details(status),
                "resource_usage": self._generate_resource_usage(),
                "performance_metrics": self._generate_execution_metrics(),
                "trace_data": self._generate_trace_data(),
                "metadata": {
                    "environment": random.choice(["development", "staging", "production"]),
                    "executor": random.choice(["system", "user", "scheduler"]),
                    "priority": random.choice(["low", "medium", "high", "critical"])
                }
            }
            
            execution_logs.append(sample)
        
        return execution_logs

    def _generate_agent_context(self, agent_name: str, agent_config: Dict) -> Dict:
        """Generate context for agent operations"""
        return {
            "current_task": random.choice(agent_config["capabilities"]),
            "system_state": self._generate_system_state(),
            "available_resources": self._generate_available_resources(),
            "constraints": self._generate_constraints(),
            "goals": self._generate_goals(agent_config["domains"])
        }

    def _generate_agent_input(self, agent_name: str, agent_config: Dict) -> str:
        """Generate realistic input for specific agent types"""
        templates = {
            "CostOptBot": [
                "Analyze current cloud infrastructure costs for the last 30 days",
                "Identify opportunities to reduce database costs",
                "Generate cost optimization recommendations for container workloads",
                "Compare costs between different cloud providers for our workload"
            ],
            "SecuBot": [
                "Perform security scan on web application endpoints",
                "Check for vulnerabilities in container images",
                "Audit network security configurations",
                "Analyze security logs for potential threats"
            ],
            "ComplianceBot": [
                "Verify GDPR compliance for data processing activities",
                "Check SOX compliance for financial data handling",
                "Audit HIPAA compliance for patient data systems",
                "Validate PCI DSS compliance for payment processing"
            ]
        }
        
        agent_templates = templates.get(agent_name, [f"Execute {agent_config['role'].lower()} task"])
        return random.choice(agent_templates)

    def _generate_agent_output(self, agent_name: str, agent_config: Dict) -> Dict:
        """Generate realistic output for specific agent types"""
        base_output = {
            "status": "completed",
            "summary": f"Successfully executed {agent_config['role'].lower()} task",
            "details": self._generate_detailed_results(agent_name),
            "recommendations": self._generate_recommendations(agent_name),
            "metrics": self._generate_task_metrics(),
            "confidence_score": random.uniform(0.7, 0.99)
        }
        
        return base_output

    def _generate_detailed_results(self, agent_name: str) -> Dict:
        """Generate detailed results based on agent type"""
        results = {
            "CostOptBot": {
                "total_cost_analyzed": f"${random.randint(10000, 100000):,}",
                "potential_savings": f"${random.randint(1000, 15000):,}",
                "optimization_opportunities": random.randint(5, 20),
                "cost_categories": ["compute", "storage", "network", "licenses"]
            },
            "SecuBot": {
                "vulnerabilities_found": random.randint(0, 15),
                "critical_issues": random.randint(0, 3),
                "security_score": random.randint(70, 95),
                "scan_coverage": f"{random.randint(85, 100)}%"
            },
            "ComplianceBot": {
                "compliance_score": random.randint(80, 100),
                "violations_found": random.randint(0, 8),
                "requirements_checked": random.randint(50, 200),
                "certification_status": random.choice(["compliant", "non-compliant", "partially_compliant"])
            }
        }
        
        return results.get(agent_name, {"generic_results": "Task completed successfully"})

    def _generate_recommendations(self, agent_name: str) -> List[str]:
        """Generate relevant recommendations for each agent type"""
        recommendations = {
            "CostOptBot": [
                "Migrate to reserved instances for consistent workloads",
                "Implement auto-scaling for dynamic resource allocation",
                "Consider spot instances for non-critical batch jobs",
                "Optimize database storage by removing unused data"
            ],
            "SecuBot": [
                "Update vulnerable dependencies immediately",
                "Enable two-factor authentication for admin accounts",
                "Implement network segmentation for sensitive systems",
                "Regular security awareness training for staff"
            ],
            "ComplianceBot": [
                "Implement data retention policies",
                "Enhance audit logging capabilities",
                "Update privacy policies to reflect current practices",
                "Conduct regular compliance assessments"
            ]
        }
        
        agent_recs = recommendations.get(agent_name, ["Continue monitoring system performance"])
        return random.sample(agent_recs, min(len(agent_recs), random.randint(2, 4)))

    def _generate_orchestration_plan(self, agents: List[str], scenario: str) -> Dict:
        """Generate orchestration plan for multi-agent scenarios"""
        return {
            "execution_order": agents,
            "parallel_stages": self._identify_parallel_stages(agents),
            "decision_points": self._generate_decision_points(scenario),
            "rollback_strategy": self._generate_rollback_strategy(),
            "success_criteria": self._generate_success_criteria(scenario)
        }

    def _generate_execution_flow(self, agents: List[str]) -> List[Dict]:
        """Generate execution flow steps"""
        flow = []
        for i, agent in enumerate(agents):
            step = {
                "step": i + 1,
                "agent": agent,
                "action": f"Execute {self.agents[agent]['role'].lower()}",
                "dependencies": agents[:i] if i > 0 else [],
                "timeout": random.randint(30, 300),
                "retry_policy": {
                    "max_attempts": random.randint(1, 3),
                    "backoff_strategy": random.choice(["linear", "exponential"])
                }
            }
            flow.append(step)
        
        return flow

    def _generate_system_metrics(self) -> Dict:
        """Generate realistic system metrics"""
        return {
            "cpu_usage": round(random.uniform(10, 90), 2),
            "memory_usage": round(random.uniform(20, 85), 2),
            "disk_usage": round(random.uniform(15, 80), 2),
            "network_io": round(random.uniform(5, 70), 2),
            "active_connections": random.randint(50, 500),
            "request_rate": random.randint(100, 2000),
            "response_time_avg": round(random.uniform(50, 500), 2),
            "error_rate": round(random.uniform(0, 5), 3)
        }

    def _generate_agent_metrics(self) -> Dict:
        """Generate agent-specific metrics"""
        return {
            agent_name: {
                "execution_count": random.randint(0, 50),
                "success_rate": round(random.uniform(0.8, 1.0), 3),
                "avg_execution_time": random.randint(1000, 10000),
                "resource_utilization": round(random.uniform(0.1, 0.8), 2),
                "queue_size": random.randint(0, 20)
            }
            for agent_name in random.sample(list(self.agents.keys()), random.randint(3, 6))
        }

    def _random_timestamp(self) -> datetime:
        """Generate random timestamp within last 90 days"""
        start_date = datetime.now() - timedelta(days=90)
        random_days = random.randint(0, 90)
        random_seconds = random.randint(0, 86400)
        return start_date + timedelta(days=random_days, seconds=random_seconds)

    def _generate_human_input(self, conv_type: str) -> str:
        """Generate realistic human input for different conversation types"""
        inputs = {
            "task_assignment": [
                "Run a cost analysis on our AWS infrastructure",
                "Please check our compliance status for GDPR",
                "I need a security scan of the production environment",
                "Can you analyze the performance of our database cluster?"
            ],
            "status_inquiry": [
                "What's the status of the security scan I requested?",
                "How is the cost optimization analysis progressing?",
                "Are there any issues with the compliance check?",
                "When will the performance analysis be complete?"
            ],
            "troubleshooting": [
                "Why did the last execution fail?",
                "I'm seeing errors in the agent logs, can you help?",
                "The system seems slow, what's causing it?",
                "Some agents are not responding, what should I do?"
            ]
        }
        
        conv_inputs = inputs.get(conv_type, ["How can I help you today?"])
        return random.choice(conv_inputs)

    def _generate_ai_response(self, conv_type: str) -> str:
        """Generate AI responses for different conversation types"""
        responses = {
            "task_assignment": [
                "I'll start the cost analysis right away. This typically takes 5-10 minutes to complete.",
                "Initiating GDPR compliance check. I'll scan all data processing activities.",
                "Security scan has been queued for execution. You'll receive results within 15 minutes.",
                "Starting database performance analysis. I'll examine query performance and resource usage."
            ],
            "status_inquiry": [
                "The security scan is 75% complete. I've found 3 minor issues so far.",
                "Cost optimization analysis is finished. I identified $12,400 in potential monthly savings.",
                "Compliance check completed successfully. You're 96% compliant with GDPR requirements.",
                "Performance analysis is still running. Current progress: 60% complete."
            ],
            "troubleshooting": [
                "The execution failed due to a timeout. The target system didn't respond within 5 minutes.",
                "I see authentication errors in the logs. Please check your API credentials.",
                "High CPU usage is causing the slowdown. Running diagnostics to identify the cause.",
                "Two agents are experiencing network connectivity issues. Attempting to restart them."
            ]
        }
        
        conv_responses = responses.get(conv_type, ["I'm here to help. What would you like me to do?"])
        return random.choice(conv_responses)

    # Additional helper methods...
    def _generate_system_state(self) -> Dict:
        return {"load": random.uniform(0.1, 0.9), "health": "healthy"}
    
    def _generate_available_resources(self) -> Dict:
        return {"cpu": random.uniform(0.2, 0.8), "memory": random.uniform(0.3, 0.7)}
    
    def _generate_constraints(self) -> List[str]:
        return random.sample(["time_limit", "resource_limit", "compliance", "security"], random.randint(1, 3))
    
    def _generate_goals(self, domains: List[str]) -> List[str]:
        return random.sample(domains, random.randint(1, len(domains)))
    
    def _generate_task_metrics(self) -> Dict:
        return {
            "execution_time": random.randint(1000, 30000),
            "resources_used": random.uniform(0.1, 0.8),
            "data_processed": random.randint(100, 10000)
        }
    
    def _identify_parallel_stages(self, agents: List[str]) -> List[List[str]]:
        # Simple logic to identify which agents can run in parallel
        if len(agents) <= 2:
            return [agents]
        
        mid = len(agents) // 2
        return [agents[:mid], agents[mid:]]
    
    def _generate_decision_points(self, scenario: str) -> List[Dict]:
        return [
            {
                "condition": f"if {scenario}_score < threshold",
                "action": "escalate_to_human",
                "threshold": random.uniform(0.5, 0.8)
            }
        ]
    
    def _generate_rollback_strategy(self) -> Dict:
        return {
            "enabled": True,
            "checkpoints": random.randint(2, 5),
            "automatic": random.choice([True, False])
        }
    
    def _generate_success_criteria(self, scenario: str) -> List[str]:
        criteria = [
            f"{scenario}_completed_successfully",
            "no_critical_errors",
            "performance_within_limits"
        ]
        return random.sample(criteria, random.randint(2, 3))
    
    def _generate_dependencies(self, agents: List[str]) -> Dict:
        deps = {}
        for i, agent in enumerate(agents[1:], 1):
            deps[agent] = random.sample(agents[:i], random.randint(0, min(2, i)))
        return deps
    
    def _generate_expected_outcomes(self, scenario: str) -> Dict:
        return {
            "primary_outcome": f"{scenario}_optimization",
            "success_probability": random.uniform(0.7, 0.95),
            "impact_score": random.uniform(0.5, 0.9)
        }
    
    def _generate_coordination_messages(self, agents: List[str]) -> List[Dict]:
        messages = []
        for i in range(random.randint(2, 6)):
            messages.append({
                "from": random.choice(agents),
                "to": random.choice([a for a in agents if a != messages[-1]["from"] if messages else agents]),
                "message": "coordination_signal",
                "timestamp": self._random_timestamp().isoformat()
            })
        return messages
    
    def _calculate_complexity(self, agents: List[str], scenario: str) -> str:
        complexity_score = len(agents) + len(scenario.split("_"))
        if complexity_score <= 3:
            return "low"
        elif complexity_score <= 6:
            return "medium"
        else:
            return "high"
    
    def _generate_resource_requirements(self) -> Dict:
        return {
            "cpu_cores": random.randint(1, 8),
            "memory_gb": random.randint(2, 16),
            "storage_gb": random.randint(10, 100),
            "network_bandwidth": f"{random.randint(100, 1000)}Mbps"
        }
    
    def _generate_performance_indicators(self) -> Dict:
        return {
            "throughput": random.randint(100, 5000),
            "latency_p95": random.uniform(10, 500),
            "availability": random.uniform(0.95, 0.999),
            "efficiency_score": random.uniform(0.7, 0.95)
        }
    
    def _calculate_health_score(self) -> float:
        return round(random.uniform(0.7, 0.99), 3)
    
    def _generate_alerts(self) -> List[Dict]:
        if random.random() < 0.3:  # 30% chance of alerts
            return [
                {
                    "id": str(uuid.uuid4()),
                    "severity": random.choice(["low", "medium", "high", "critical"]),
                    "message": random.choice([
                        "High CPU usage detected",
                        "Memory usage approaching limit",
                        "Unusual network activity",
                        "Agent execution failure"
                    ]),
                    "timestamp": self._random_timestamp().isoformat()
                }
            ]
        return []
    
    def _generate_trends(self) -> Dict:
        return {
            "cpu_trend": random.choice(["increasing", "decreasing", "stable"]),
            "memory_trend": random.choice(["increasing", "decreasing", "stable"]),
            "performance_trend": random.choice(["improving", "degrading", "stable"])
        }
    
    def _detect_anomalies(self) -> List[Dict]:
        if random.random() < 0.2:  # 20% chance of anomalies
            return [
                {
                    "type": random.choice(["performance", "resource", "behavior"]),
                    "description": "Unusual pattern detected",
                    "confidence": random.uniform(0.6, 0.9),
                    "timestamp": self._random_timestamp().isoformat()
                }
            ]
        return []
    
    def _generate_conversation_context(self, conv_type: str) -> Dict:
        return {
            "session_id": str(uuid.uuid4()),
            "user_role": random.choice(["admin", "operator", "analyst"]),
            "system_state": "operational",
            "active_agents": random.randint(3, 8)
        }
    
    def _extract_intent(self, conv_type: str) -> str:
        intents = {
            "task_assignment": "assign_task",
            "status_inquiry": "check_status", 
            "troubleshooting": "resolve_issue",
            "configuration": "configure_system",
            "analysis_request": "analyze_data",
            "reporting": "generate_report"
        }
        return intents.get(conv_type, "general_inquiry")
    
    def _extract_entities(self, conv_type: str) -> List[Dict]:
        entities = [
            {"type": "agent", "value": random.choice(list(self.agents.keys()))},
            {"type": "timeframe", "value": random.choice(["last_hour", "today", "this_week"])},
            {"type": "metric", "value": random.choice(self.metric_templates)}
        ]
        return random.sample(entities, random.randint(1, 3))
    
    def _analyze_sentiment(self) -> Dict:
        return {
            "score": random.uniform(-1, 1),
            "label": random.choice(["positive", "neutral", "negative"]),
            "confidence": random.uniform(0.6, 0.95)
        }
    
    def _generate_follow_up_actions(self, conv_type: str) -> List[str]:
        actions = {
            "task_assignment": ["monitor_progress", "send_notification"],
            "status_inquiry": ["provide_updates", "schedule_follow_up"],
            "troubleshooting": ["escalate_if_needed", "document_solution"]
        }
        return actions.get(conv_type, ["no_action_required"])
    
    def _generate_input_parameters(self, agent_name: str) -> Dict:
        return {
            "target_environment": random.choice(["production", "staging", "development"]),
            "scope": random.choice(["full", "partial", "targeted"]),
            "priority": random.choice(["low", "medium", "high"]),
            "max_duration": random.randint(60, 3600)
        }
    
    def _generate_output_data(self, agent_name: str, status: str) -> Dict:
        if status == "success":
            return {
                "results": self._generate_detailed_results(agent_name),
                "data_quality": random.uniform(0.8, 1.0),
                "completeness": random.uniform(0.9, 1.0)
            }
        else:
            return {"error": "Execution failed", "partial_results": None}
    
    def _generate_error_details(self, status: str) -> Optional[Dict]:
        if status in ["failed", "error", "timeout"]:
            return {
                "error_code": random.choice(["E001", "E002", "E003", "E004"]),
                "error_message": random.choice([
                    "Connection timeout",
                    "Authentication failed", 
                    "Resource not found",
                    "Permission denied"
                ]),
                "stack_trace": "Traceback (most recent call last)..."
            }
        return None
    
    def _generate_resource_usage(self) -> Dict:
        return {
            "cpu_time": random.uniform(0.1, 5.0),
            "memory_peak": random.randint(50, 500),
            "disk_io": random.randint(10, 1000),
            "network_io": random.randint(5, 500)
        }
    
    def _generate_execution_metrics(self) -> Dict:
        return {
            "operations_count": random.randint(10, 1000),
            "cache_hit_ratio": random.uniform(0.7, 0.95),
            "api_calls": random.randint(5, 100),
            "data_processed_mb": random.uniform(1, 100)
        }
    
    def _generate_trace_data(self) -> List[Dict]:
        traces = []
        for i in range(random.randint(3, 10)):
            traces.append({
                "span_id": str(uuid.uuid4()),
                "operation": f"operation_{i+1}",
                "duration_ms": random.randint(10, 1000),
                "status": random.choice(["success", "error"]),
                "tags": {"component": "agent", "version": "v1.0"}
            })
        return traces

    def save_datasets(self):
        """Generate and save all datasets to JSONL files"""
        
        print("Generating AI Operating System Training Datasets...")
        
        # Generate datasets
        datasets = {
            "agent_training": self.generate_agent_training_data(1000),
            "system_interactions": self.generate_system_interaction_data(500),
            "monitoring_data": self.generate_monitoring_data(2000),
            "conversations": self.generate_conversation_data(800),
            "execution_logs": self.generate_execution_logs(1500)
        }
        
        # Save to JSONL files
        for dataset_name, data in datasets.items():
            filepath = self.output_dir / f"{dataset_name}.jsonl"
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
            print(f"✅ Saved {len(data)} samples to {filepath}")
        
        # Generate summary statistics
        self._generate_dataset_summary(datasets)
        
        print(f"\n🎉 All datasets generated successfully in {self.output_dir}/")

    def _generate_dataset_summary(self, datasets: Dict[str, List[Dict]]):
        """Generate summary statistics for all datasets"""
        
        summary = {
            "generation_timestamp": datetime.now().isoformat(),
            "total_samples": sum(len(data) for data in datasets.values()),
            "datasets": {}
        }
        
        for name, data in datasets.items():
            summary["datasets"][name] = {
                "sample_count": len(data),
                "date_range": {
                    "start": min(item["timestamp"] for item in data),
                    "end": max(item["timestamp"] for item in data)
                },
                "unique_agents": len(set(
                    item.get("agent", item.get("agent_name", "unknown")) 
                    for item in data 
                    if "agent" in item or "agent_name" in item
                )),
                "avg_sample_size": sum(len(json.dumps(item)) for item in data) / len(data)
            }
        
        # Save summary
        with open(self.output_dir / "dataset_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Dataset summary saved to {self.output_dir}/dataset_summary.json")

if __name__ == "__main__":
    generator = DatasetGenerator()
    generator.save_datasets()
