from core.plugin_interface import PluginInterface
import json
import os
from datetime import datetime

class ArchitectureDesignerAgent(PluginInterface):
    def __init__(self):
        self.name = "ArchitectureDesignerAgent"
        self.role = "Architecture Designer Agent"
        self.description = "Plans high-level design patterns and scaling strategy for the AI system"
        self.architecture_patterns = []
        self.scaling_recommendations = []
    
    def run(self):
        print(f"🤖 {self.name} ({self.role}) is analyzing system architecture...")
        
        # Analyze current architecture
        current_architecture = self.analyze_current_architecture()
        
        # Design future architecture
        future_architecture = self.design_future_architecture()
        
        # Create scaling strategy
        scaling_strategy = self.create_scaling_strategy()
        
        # Generate migration plan
        migration_plan = self.generate_migration_plan(current_architecture, future_architecture)
        
        # Create comprehensive architecture document
        architecture_design = self.create_architecture_document(
            current_architecture, future_architecture, scaling_strategy, migration_plan
        )
        
        print(f"✅ {self.name} completed architecture analysis and design")
        return architecture_design
    
    def analyze_current_architecture(self):
        """Analyze the current system architecture"""
        analysis = {
            "architecture_style": self.identify_architecture_style(),
            "components": self.catalog_components(),
            "data_flow": self.analyze_data_flow(),
            "integration_points": self.identify_integration_points(),
            "scalability_assessment": self.assess_current_scalability(),
            "reliability_assessment": self.assess_reliability()
        }
        
        print(f"🏗️ Analyzed current architecture")
        return analysis
    
    def identify_architecture_style(self):
        """Identify the current architectural style"""
        styles = {
            "primary": "Microservices with Plugin Architecture",
            "secondary": "Event-Driven Architecture",
            "patterns": []
        }
        
        # Check for plugin pattern
        if os.path.exists('plugins') and os.path.exists('core/plugin_interface.py'):
            styles["patterns"].append({
                "pattern": "Plugin Architecture",
                "evidence": "Dedicated plugins directory with interface definition",
                "benefits": ["Extensibility", "Modularity", "Separation of concerns"]
            })
        
        # Check for service pattern
        if os.path.exists('services'):
            styles["patterns"].append({
                "pattern": "Service-Oriented Architecture",
                "evidence": "Dedicated services directory",
                "benefits": ["Service isolation", "Independent deployment", "Technology diversity"]
            })
        
        # Check for layered architecture
        if os.path.exists('core'):
            styles["patterns"].append({
                "pattern": "Layered Architecture",
                "evidence": "Core layer with business logic separation",
                "benefits": ["Clear separation", "Reusability", "Maintainability"]
            })
        
        return styles
    
    def catalog_components(self):
        """Catalog all system components"""
        components = {
            "core_components": [],
            "agents": [],
            "services": [],
            "utilities": [],
            "data_stores": []
        }
        
        # Core components
        if os.path.exists('core'):
            for file in os.listdir('core'):
                if file.endswith('.py'):
                    components["core_components"].append({
                        "name": file.replace('.py', ''),
                        "type": "Core Module",
                        "responsibility": self.infer_component_responsibility(f"core/{file}")
                    })
        
        # Agent components
        if os.path.exists('plugins'):
            for plugin_dir in os.listdir('plugins'):
                if os.path.isdir(os.path.join('plugins', plugin_dir)):
                    components["agents"].append({
                        "name": plugin_dir,
                        "type": "AI Agent",
                        "responsibility": self.infer_agent_responsibility(plugin_dir)
                    })
        
        # Service components
        if os.path.exists('services'):
            for service_dir in os.listdir('services'):
                if os.path.isdir(os.path.join('services', service_dir)):
                    components["services"].append({
                        "name": service_dir,
                        "type": "Microservice",
                        "responsibility": self.infer_service_responsibility(service_dir)
                    })
        
        # Data stores
        data_files = ['ai-agents-manifest.json', 'requirements.txt']
        if os.path.exists('services/prompt_memory/prompts.json'):
            data_files.append('services/prompt_memory/prompts.json')
        
        for data_file in data_files:
            if os.path.exists(data_file):
                components["data_stores"].append({
                    "name": data_file,
                    "type": "Data Store",
                    "format": data_file.split('.')[-1].upper()
                })
        
        return components
    
    def infer_component_responsibility(self, file_path):
        """Infer component responsibility from file name and content"""
        file_name = os.path.basename(file_path).replace('.py', '')
        
        responsibility_map = {
            'plugin_manager': 'Manages plugin lifecycle and discovery',
            'plugin_interface': 'Defines plugin contract and interface',
            'config_manager': 'Handles configuration management',
            'logger': 'Provides logging functionality',
            'event_bus': 'Manages event-driven communication'
        }
        
        return responsibility_map.get(file_name, f"Handles {file_name.replace('_', ' ')} functionality")
    
    def infer_agent_responsibility(self, agent_dir):
        """Infer agent responsibility from directory name"""
        responsibility_map = {
            'cost_optimization_agent': 'Analyzes and optimizes infrastructure costs',
            'compliance_agent': 'Ensures regulatory compliance',
            'security_agent': 'Performs security analysis and hardening',
            'testing_agent': 'Automates testing and quality assurance',
            'privacy_agent': 'Manages data privacy and protection',
            'insights_agent': 'Generates analytics and insights',
            'conversation_design_agent': 'Designs conversational interfaces',
            'model_refactor_agent': 'Refactors and optimizes code',
            'architecture_agent': 'Designs system architecture'
        }
        
        return responsibility_map.get(agent_dir, f"Handles {agent_dir.replace('_', ' ')} functionality")
    
    def infer_service_responsibility(self, service_dir):
        """Infer service responsibility from directory name"""
        responsibility_map = {
            'prompt_memory': 'Stores and retrieves AI prompts',
            'api_gateway': 'Routes and manages API requests',
            'auth_service': 'Handles authentication and authorization',
            'notification_service': 'Manages system notifications'
        }
        
        return responsibility_map.get(service_dir, f"Provides {service_dir.replace('_', ' ')} functionality")
    
    def analyze_data_flow(self):
        """Analyze how data flows through the system"""
        flow = {
            "entry_points": [],
            "processing_stages": [],
            "output_channels": [],
            "data_transformations": []
        }
        
        # Entry points
        flow["entry_points"].extend([
            {"type": "CLI", "description": "Command-line interface via main.py"},
            {"type": "API", "description": "REST API via Flask services"},
            {"type": "File", "description": "Configuration files and data inputs"}
        ])
        
        # Processing stages
        flow["processing_stages"].extend([
            {"stage": "Discovery", "description": "Plugin manager discovers and loads agents"},
            {"stage": "Execution", "description": "Agents execute their analysis and processing"},
            {"stage": "Aggregation", "description": "Results are collected and consolidated"},
            {"stage": "Reporting", "description": "Outputs are generated and stored"}
        ])
        
        # Output channels
        flow["output_channels"].extend([
            {"type": "Reports", "description": "JSON and Markdown reports in reports/ directory"},
            {"type": "Logs", "description": "Console output and log files"},
            {"type": "API", "description": "REST API responses"}
        ])
        
        return flow
    
    def identify_integration_points(self):
        """Identify system integration points"""
        integrations = {
            "internal_integrations": [],
            "external_integrations": [],
            "api_endpoints": [],
            "data_interfaces": []
        }
        
        # Internal integrations
        integrations["internal_integrations"].extend([
            {"components": ["Plugin Manager", "Agents"], "type": "Interface-based"},
            {"components": ["Agents", "Report Generator"], "type": "Data-driven"},
            {"components": ["Services", "Core"], "type": "API-based"}
        ])
        
        # External integrations (potential)
        integrations["external_integrations"].extend([
            {"system": "Cloud Providers", "purpose": "Cost analysis and resource monitoring"},
            {"system": "CI/CD Systems", "purpose": "Automated testing and deployment"},
            {"system": "Monitoring Tools", "purpose": "System health and performance tracking"},
            {"system": "Identity Providers", "purpose": "Authentication and authorization"}
        ])
        
        # API endpoints
        if os.path.exists('services/prompt_memory/app.py'):
            integrations["api_endpoints"].extend([
                {"service": "Prompt Memory", "endpoints": ["/add", "/search", "/prompts"]},
            ])
        
        return integrations
    
    def assess_current_scalability(self):
        """Assess current system scalability"""
        assessment = {
            "horizontal_scalability": "Good",
            "vertical_scalability": "Limited",
            "bottlenecks": [],
            "scalability_score": 75,
            "recommendations": []
        }
        
        # Identify potential bottlenecks
        assessment["bottlenecks"].extend([
            {"component": "File-based storage", "impact": "Medium", "description": "JSON files don't scale well"},
            {"component": "Synchronous execution", "impact": "High", "description": "Agents run sequentially"},
            {"component": "Memory usage", "impact": "Medium", "description": "All data loaded in memory"}
        ])
        
        # Scalability recommendations
        assessment["recommendations"].extend([
            "Implement database storage for better data management",
            "Add asynchronous agent execution",
            "Implement caching layers for frequently accessed data",
            "Create horizontal scaling for agent workers"
        ])
        
        return assessment
    
    def assess_reliability(self):
        """Assess system reliability"""
        assessment = {
            "fault_tolerance": "Basic",
            "error_handling": "Partial",
            "recovery_mechanisms": "Limited",
            "reliability_score": 65,
            "improvements": []
        }
        
        # Reliability improvements
        assessment["improvements"].extend([
            "Implement comprehensive error handling and recovery",
            "Add health checks and monitoring",
            "Create backup and restore mechanisms",
            "Implement circuit breakers for external dependencies"
        ])
        
        return assessment
    
    def design_future_architecture(self):
        """Design the future architecture"""
        future_arch = {
            "target_architecture": "Cloud-Native Microservices with Event-Driven Architecture",
            "key_improvements": self.identify_key_improvements(),
            "component_design": self.design_future_components(),
            "technology_stack": self.recommend_technology_stack(),
            "deployment_model": self.design_deployment_model()
        }
        
        print(f"🚀 Designed future architecture")
        return future_arch
    
    def identify_key_improvements(self):
        """Identify key architectural improvements"""
        return [
            {
                "area": "Scalability",
                "improvement": "Container-based deployment with auto-scaling",
                "benefit": "Handle variable workloads efficiently"
            },
            {
                "area": "Reliability",
                "improvement": "Distributed architecture with redundancy",
                "benefit": "Eliminate single points of failure"
            },
            {
                "area": "Performance",
                "improvement": "Asynchronous processing and caching",
                "benefit": "Improve response times and throughput"
            },
            {
                "area": "Observability",
                "improvement": "Comprehensive monitoring and logging",
                "benefit": "Better system visibility and debugging"
            },
            {
                "area": "Security",
                "improvement": "Zero-trust security model",
                "benefit": "Enhanced security posture"
            }
        ]
    
    def design_future_components(self):
        """Design future system components"""
        return {
            "api_gateway": {
                "purpose": "Central entry point for all requests",
                "features": ["Rate limiting", "Authentication", "Routing", "Load balancing"]
            },
            "agent_orchestrator": {
                "purpose": "Manages agent execution and coordination",
                "features": ["Task queuing", "Dependency management", "Parallel execution"]
            },
            "event_bus": {
                "purpose": "Enables event-driven communication",
                "features": ["Pub/Sub messaging", "Event sourcing", "Real-time updates"]
            },
            "data_layer": {
                "purpose": "Persistent data storage and management",
                "features": ["Database abstraction", "Caching", "Data versioning"]
            },
            "monitoring_service": {
                "purpose": "System observability and health monitoring",
                "features": ["Metrics collection", "Alerting", "Distributed tracing"]
            }
        }
    
    def recommend_technology_stack(self):
        """Recommend technology stack for future architecture"""
        return {
            "runtime": {
                "primary": "Python 3.11+",
                "async": "AsyncIO",
                "packaging": "Docker containers"
            },
            "data_storage": {
                "primary": "PostgreSQL",
                "cache": "Redis",
                "search": "Elasticsearch"
            },
            "messaging": {
                "event_bus": "Apache Kafka",
                "task_queue": "Celery",
                "real_time": "WebSockets"
            },
            "infrastructure": {
                "orchestration": "Kubernetes",
                "service_mesh": "Istio",
                "ingress": "Nginx"
            },
            "observability": {
                "metrics": "Prometheus",
                "logging": "ELK Stack",
                "tracing": "Jaeger"
            }
        }
    
    def design_deployment_model(self):
        """Design deployment model"""
        return {
            "deployment_strategy": "Blue-Green with Canary Releases",
            "environments": ["Development", "Staging", "Production"],
            "scaling_strategy": {
                "agents": "Horizontal pod autoscaling based on CPU/memory",
                "services": "Vertical and horizontal scaling based on load",
                "data": "Read replicas and sharding for high throughput"
            },
            "disaster_recovery": {
                "backup_strategy": "Automated daily backups with point-in-time recovery",
                "failover": "Multi-region deployment with automatic failover",
                "rto": "< 15 minutes",
                "rpo": "< 5 minutes"
            }
        }
    
    def create_scaling_strategy(self):
        """Create comprehensive scaling strategy"""
        strategy = {
            "current_limitations": self.identify_scaling_limitations(),
            "scaling_dimensions": self.define_scaling_dimensions(),
            "implementation_phases": self.plan_scaling_implementation(),
            "capacity_planning": self.create_capacity_plan()
        }
        
        print(f"📈 Created scaling strategy")
        return strategy
    
    def identify_scaling_limitations(self):
        """Identify current scaling limitations"""
        return [
            {"limitation": "Sequential agent execution", "impact": "High", "solution": "Parallel execution"},
            {"limitation": "File-based storage", "impact": "Medium", "solution": "Database migration"},
            {"limitation": "Monolithic deployment", "impact": "Medium", "solution": "Containerization"},
            {"limitation": "No load balancing", "impact": "High", "solution": "Load balancer implementation"}
        ]
    
    def define_scaling_dimensions(self):
        """Define different scaling dimensions"""
        return {
            "compute_scaling": {
                "horizontal": "Add more agent worker nodes",
                "vertical": "Increase CPU/memory per node",
                "triggers": ["CPU > 70%", "Memory > 80%", "Queue depth > 100"]
            },
            "data_scaling": {
                "read_scaling": "Read replicas for query distribution",
                "write_scaling": "Sharding for write distribution",
                "storage_scaling": "Automated storage expansion"
            },
            "network_scaling": {
                "cdn": "Content delivery network for static assets",
                "load_balancing": "Geographic load distribution",
                "bandwidth": "Adaptive bandwidth allocation"
            }
        }
    
    def plan_scaling_implementation(self):
        """Plan scaling implementation phases"""
        return [
            {
                "phase": "Phase 1: Containerization",
                "duration": "4-6 weeks",
                "goals": ["Containerize all components", "Implement basic orchestration"],
                "deliverables": ["Docker images", "Kubernetes manifests", "CI/CD pipeline"]
            },
            {
                "phase": "Phase 2: Microservices",
                "duration": "6-8 weeks",
                "goals": ["Break monolith into services", "Implement service mesh"],
                "deliverables": ["Service definitions", "API contracts", "Service mesh configuration"]
            },
            {
                "phase": "Phase 3: Auto-scaling",
                "duration": "4-6 weeks",
                "goals": ["Implement auto-scaling", "Add monitoring"],
                "deliverables": ["Scaling policies", "Monitoring dashboards", "Alerting rules"]
            }
        ]
    
    def create_capacity_plan(self):
        """Create capacity planning guidelines"""
        return {
            "baseline_requirements": {
                "cpu": "4 cores",
                "memory": "8GB",
                "storage": "100GB",
                "network": "1Gbps"
            },
            "scaling_factors": {
                "agents": "Linear scaling with agent count",
                "data": "Logarithmic scaling with data volume",
                "users": "Linear scaling with concurrent users"
            },
            "capacity_thresholds": {
                "scale_up": {"cpu": "70%", "memory": "80%", "disk": "85%"},
                "scale_down": {"cpu": "30%", "memory": "40%", "disk": "50%"}
            }
        }
    
    def generate_migration_plan(self, current_arch, future_arch):
        """Generate migration plan from current to future architecture"""
        plan = {
            "migration_strategy": "Incremental Migration with Strangler Fig Pattern",
            "migration_phases": self.create_migration_phases(),
            "risk_assessment": self.assess_migration_risks(),
            "rollback_strategy": self.define_rollback_strategy()
        }
        
        print(f"🔄 Generated migration plan")
        return plan
    
    def create_migration_phases(self):
        """Create detailed migration phases"""
        return [
            {
                "phase": 1,
                "name": "Infrastructure Preparation",
                "duration": "2-3 weeks",
                "description": "Set up target infrastructure and tooling",
                "tasks": [
                    "Set up Kubernetes cluster",
                    "Configure CI/CD pipelines",
                    "Implement monitoring stack",
                    "Set up development environments"
                ],
                "success_criteria": ["Infrastructure ready", "Pipelines functional", "Monitoring active"]
            },
            {
                "phase": 2,
                "name": "Core Services Migration",
                "duration": "4-6 weeks",
                "description": "Migrate core services to new architecture",
                "tasks": [
                    "Containerize existing services",
                    "Implement database migration",
                    "Set up service mesh",
                    "Configure load balancing"
                ],
                "success_criteria": ["Services running in containers", "Database migrated", "Mesh operational"]
            },
            {
                "phase": 3,
                "name": "Agent System Modernization",
                "duration": "6-8 weeks",
                "description": "Modernize agent execution and management",
                "tasks": [
                    "Implement agent orchestrator",
                    "Add asynchronous execution",
                    "Create event-driven communication",
                    "Implement auto-scaling"
                ],
                "success_criteria": ["Orchestrator functional", "Async execution", "Events working", "Auto-scaling active"]
            },
            {
                "phase": 4,
                "name": "Advanced Features",
                "duration": "4-6 weeks",
                "description": "Add advanced capabilities and optimization",
                "tasks": [
                    "Implement advanced caching",
                    "Add machine learning capabilities",
                    "Create advanced analytics",
                    "Implement security enhancements"
                ],
                "success_criteria": ["Caching optimized", "ML integrated", "Analytics enhanced", "Security hardened"]
            }
        ]
    
    def assess_migration_risks(self):
        """Assess migration risks and mitigation strategies"""
        return [
            {
                "risk": "Service downtime during migration",
                "probability": "Medium",
                "impact": "High",
                "mitigation": "Blue-green deployment with rollback capability"
            },
            {
                "risk": "Data loss during database migration",
                "probability": "Low",
                "impact": "Critical",
                "mitigation": "Comprehensive backup and testing strategy"
            },
            {
                "risk": "Performance degradation",
                "probability": "Medium",
                "impact": "Medium",
                "mitigation": "Thorough performance testing and optimization"
            },
            {
                "risk": "Integration failures",
                "probability": "High",
                "impact": "Medium",
                "mitigation": "Extensive integration testing and monitoring"
            }
        ]
    
    def define_rollback_strategy(self):
        """Define rollback strategy for failed migrations"""
        return {
            "rollback_triggers": [
                "System availability < 95%",
                "Performance degradation > 50%",
                "Critical functionality failures",
                "Data integrity issues"
            ],
            "rollback_procedures": [
                "Immediate traffic redirection to old system",
                "Database state restoration from backup",
                "Service configuration rollback",
                "Post-incident analysis and reporting"
            ],
            "rollback_time_targets": {
                "detection": "< 5 minutes",
                "decision": "< 10 minutes",
                "execution": "< 30 minutes",
                "verification": "< 15 minutes"
            }
        }
    
    def create_architecture_document(self, current_arch, future_arch, scaling_strategy, migration_plan):
        """Create comprehensive architecture document"""
        document = {
            "timestamp": datetime.now().isoformat(),
            "executive_summary": self.create_executive_summary(),
            "current_architecture": current_arch,
            "future_architecture": future_arch,
            "scaling_strategy": scaling_strategy,
            "migration_plan": migration_plan,
            "recommendations": self.create_architecture_recommendations()
        }
        
        # Save the document
        doc_path = "reports/architecture_design.json"
        os.makedirs(os.path.dirname(doc_path), exist_ok=True)
        
        with open(doc_path, 'w') as f:
            json.dump(document, f, indent=2)
        
        print(f"📄 Architecture document saved to: {doc_path}")
        
        # Generate architecture blueprint
        self.generate_architecture_blueprint(document)
        
        return document
    
    def create_executive_summary(self):
        """Create executive summary of architecture analysis"""
        return {
            "current_state": "Plugin-based microservices architecture with good modularity",
            "target_state": "Cloud-native, event-driven architecture with auto-scaling",
            "key_benefits": [
                "10x improvement in scalability",
                "50% reduction in operational overhead",
                "Enhanced reliability and fault tolerance",
                "Improved developer productivity"
            ],
            "investment_required": "12-16 weeks development effort",
            "recommended_timeline": "4-phase migration over 6 months"
        }
    
    def create_architecture_recommendations(self):
        """Create architecture recommendations"""
        return [
            {
                "category": "Immediate Actions",
                "priority": "High",
                "recommendations": [
                    "Begin containerization of existing services",
                    "Implement comprehensive monitoring",
                    "Set up development/staging environments",
                    "Create architectural documentation"
                ]
            },
            {
                "category": "Short-term (3-6 months)",
                "priority": "High",
                "recommendations": [
                    "Complete microservices migration",
                    "Implement event-driven architecture",
                    "Add auto-scaling capabilities",
                    "Enhance security posture"
                ]
            },
            {
                "category": "Long-term (6-12 months)",
                "priority": "Medium",
                "recommendations": [
                    "Implement advanced analytics",
                    "Add machine learning capabilities",
                    "Create multi-region deployment",
                    "Optimize for cost efficiency"
                ]
            }
        ]
    
    def generate_architecture_blueprint(self, document):
        """Generate architecture blueprint in markdown"""
        blueprint_path = "docs/architecture_blueprint.md"
        os.makedirs(os.path.dirname(blueprint_path), exist_ok=True)
        
        with open(blueprint_path, 'w') as f:
            f.write("# Architecture Blueprint\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            summary = document["executive_summary"]
            f.write("## 📋 Executive Summary\n\n")
            f.write(f"**Current State**: {summary['current_state']}\n\n")
            f.write(f"**Target State**: {summary['target_state']}\n\n")
            f.write("**Key Benefits**:\n")
            for benefit in summary['key_benefits']:
                f.write(f"- {benefit}\n")
            f.write(f"\n**Timeline**: {summary['recommended_timeline']}\n\n")
            
            # Current vs Future Architecture
            f.write("## 🏗️ Architecture Comparison\n\n")
            f.write("| Aspect | Current | Future |\n")
            f.write("|--------|---------|--------|\n")
            f.write("| Style | Plugin-based | Cloud-native microservices |\n")
            f.write("| Deployment | Single process | Container orchestration |\n")
            f.write("| Scaling | Manual | Auto-scaling |\n")
            f.write("| Communication | Direct calls | Event-driven |\n")
            f.write("| Data Storage | File-based | Database + caching |\n")
            f.write("| Monitoring | Basic logging | Comprehensive observability |\n\n")
            
            # Migration Phases
            f.write("## 🚀 Migration Roadmap\n\n")
            for phase in document["migration_plan"]["migration_phases"]:
                f.write(f"### Phase {phase['phase']}: {phase['name']}\n")
                f.write(f"**Duration**: {phase['duration']}\n\n")
                f.write(f"**Description**: {phase['description']}\n\n")
                f.write("**Key Tasks**:\n")
                for task in phase['tasks']:
                    f.write(f"- [ ] {task}\n")
                f.write("\n")
            
            # Technology Stack
            tech_stack = document["future_architecture"]["technology_stack"]
            f.write("## 🛠️ Recommended Technology Stack\n\n")
            for category, technologies in tech_stack.items():
                f.write(f"### {category.replace('_', ' ').title()}\n")
                for tech_type, tech_name in technologies.items():
                    f.write(f"- **{tech_type.replace('_', ' ').title()}**: {tech_name}\n")
                f.write("\n")
            
            # Risk Assessment
            f.write("## ⚠️ Risk Assessment\n\n")
            for risk in document["migration_plan"]["risk_assessment"]:
                f.write(f"### {risk['risk']}\n")
                f.write(f"- **Probability**: {risk['probability']}\n")
                f.write(f"- **Impact**: {risk['impact']}\n")
                f.write(f"- **Mitigation**: {risk['mitigation']}\n\n")
            
            f.write("---\n")
            f.write("*Blueprint generated by ArchitectureDesignerAgent - Review and update quarterly*\n")
        
        print(f"📐 Architecture blueprint saved to: {blueprint_path}")
    
    def get_metrics(self):
        """Return performance metrics for this agent"""
        return {
            "architecture_patterns_analyzed": len(self.architecture_patterns),
            "scaling_recommendations": len(self.scaling_recommendations),
            "last_run": datetime.now().isoformat()
        }

def get_plugin():
    return ArchitectureDesignerAgent()
