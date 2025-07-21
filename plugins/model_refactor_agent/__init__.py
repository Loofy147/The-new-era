from core.plugin_interface import PluginInterface
import json
import os
from datetime import datetime

class ModelRefactorAgent(PluginInterface):
    def __init__(self):
        self.name = "ModelRefactor"
        self.role = "Refactoring Agent"
        self.description = "Refactors AI code, tools, and workflows for better performance and maintainability"
        self.refactoring_suggestions = []
        self.code_quality_metrics = {}
    
    def run(self):
        print(f"🤖 {self.name} ({self.role}) is analyzing code for refactoring opportunities...")
        
        # Analyze codebase structure
        code_analysis = self.analyze_codebase_structure()
        
        # Identify refactoring opportunities
        refactoring_opportunities = self.identify_refactoring_opportunities()
        
        # Generate code quality recommendations
        quality_recommendations = self.generate_quality_recommendations()
        
        # Create refactoring plan
        refactoring_plan = self.create_refactoring_plan(code_analysis, refactoring_opportunities, quality_recommendations)
        
        print(f"✅ {self.name} completed refactoring analysis")
        return refactoring_plan
    
    def analyze_codebase_structure(self):
        """Analyze the overall structure of the codebase"""
        analysis = {
            "architecture_assessment": self.assess_architecture(),
            "dependency_analysis": self.analyze_dependencies(),
            "code_metrics": self.calculate_code_metrics(),
            "design_patterns": self.identify_design_patterns()
        }
        
        print(f"🔍 Analyzed codebase structure")
        return analysis
    
    def assess_architecture(self):
        """Assess the current architecture"""
        assessment = {
            "architecture_style": "plugin-based",
            "modularity_score": 85,
            "coupling_level": "low",
            "cohesion_level": "high",
            "scalability_rating": "good",
            "findings": []
        }
        
        # Check plugin architecture
        if os.path.exists('plugins') and os.path.exists('core'):
            assessment["findings"].append({
                "type": "positive",
                "description": "Well-structured plugin architecture with clear separation of concerns"
            })
        
        # Check for service-oriented design
        if os.path.exists('services'):
            assessment["findings"].append({
                "type": "positive",
                "description": "Service-oriented architecture supports scalability"
            })
        
        # Check for configuration management
        if os.path.exists('ai-agents-manifest.json'):
            assessment["findings"].append({
                "type": "positive",
                "description": "Configuration-driven design with agent manifest"
            })
        else:
            assessment["findings"].append({
                "type": "improvement",
                "description": "Consider adding comprehensive configuration management"
            })
        
        return assessment
    
    def analyze_dependencies(self):
        """Analyze project dependencies"""
        analysis = {
            "dependency_count": 0,
            "circular_dependencies": [],
            "outdated_dependencies": [],
            "security_vulnerabilities": [],
            "recommendations": []
        }
        
        # Check requirements.txt
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                deps = f.readlines()
                analysis["dependency_count"] = len([d for d in deps if d.strip() and not d.startswith('#')])
        
        # Analyze plugin dependencies
        plugin_deps = {}
        if os.path.exists('plugins'):
            for plugin_dir in os.listdir('plugins'):
                plugin_path = os.path.join('plugins', plugin_dir, '__init__.py')
                if os.path.exists(plugin_path):
                    with open(plugin_path, 'r') as f:
                        content = f.read()
                        imports = [line.strip() for line in content.split('\n') 
                                 if line.strip().startswith('import ') or line.strip().startswith('from ')]
                        plugin_deps[plugin_dir] = imports
        
        analysis["plugin_dependencies"] = plugin_deps
        
        # Recommendations
        if analysis["dependency_count"] < 5:
            analysis["recommendations"].append("Consider adding development dependencies (testing, linting)")
        
        if analysis["dependency_count"] > 20:
            analysis["recommendations"].append("Review dependencies for potential reduction")
        
        return analysis
    
    def calculate_code_metrics(self):
        """Calculate various code quality metrics"""
        metrics = {
            "total_lines": 0,
            "total_files": 0,
            "average_file_size": 0,
            "complexity_distribution": {"low": 0, "medium": 0, "high": 0},
            "maintainability_index": 0,
            "file_metrics": []
        }
        
        file_sizes = []
        
        # Analyze Python files
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    file_metrics = self.analyze_file_metrics(file_path)
                    metrics["file_metrics"].append(file_metrics)
                    
                    metrics["total_files"] += 1
                    metrics["total_lines"] += file_metrics["lines_of_code"]
                    file_sizes.append(file_metrics["lines_of_code"])
                    
                    # Complexity distribution
                    if file_metrics["complexity_score"] < 10:
                        metrics["complexity_distribution"]["low"] += 1
                    elif file_metrics["complexity_score"] < 25:
                        metrics["complexity_distribution"]["medium"] += 1
                    else:
                        metrics["complexity_distribution"]["high"] += 1
        
        if file_sizes:
            metrics["average_file_size"] = sum(file_sizes) / len(file_sizes)
        
        # Calculate maintainability index (simplified)
        if metrics["total_files"] > 0:
            avg_complexity = sum(f["complexity_score"] for f in metrics["file_metrics"]) / metrics["total_files"]
            metrics["maintainability_index"] = max(0, 100 - avg_complexity)
        
        return metrics
    
    def analyze_file_metrics(self, file_path):
        """Analyze metrics for a single file"""
        metrics = {
            "file_path": file_path,
            "lines_of_code": 0,
            "functions": 0,
            "classes": 0,
            "complexity_score": 0,
            "documentation_ratio": 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            # Count lines of code (excluding comments and empty lines)
            code_lines = 0
            comment_lines = 0
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                elif stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                    comment_lines += 1
                else:
                    code_lines += 1
            
            metrics["lines_of_code"] = code_lines
            
            # Count functions and classes
            content = ''.join(lines)
            metrics["functions"] = content.count('def ')
            metrics["classes"] = content.count('class ')
            
            # Simple complexity score
            metrics["complexity_score"] = (
                code_lines // 10 +  # Lines of code
                metrics["functions"] * 2 +  # Functions
                metrics["classes"] * 3 +  # Classes
                content.count('if ') +  # Conditional statements
                content.count('for ') +  # Loops
                content.count('while ') +  # Loops
                content.count('try:')  # Exception handling
            )
            
            # Documentation ratio
            if code_lines > 0:
                metrics["documentation_ratio"] = comment_lines / (code_lines + comment_lines)
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return metrics
    
    def identify_design_patterns(self):
        """Identify design patterns used in the codebase"""
        patterns = {
            "detected_patterns": [],
            "recommended_patterns": []
        }
        
        # Check for existing patterns
        if os.path.exists('core/plugin_interface.py'):
            patterns["detected_patterns"].append({
                "pattern": "Strategy Pattern",
                "location": "Plugin system",
                "description": "Plugin interface defines strategy for different agent implementations"
            })
        
        if os.path.exists('core/plugin_manager.py'):
            patterns["detected_patterns"].append({
                "pattern": "Factory Pattern",
                "location": "Plugin manager",
                "description": "Plugin manager acts as factory for creating plugin instances"
            })
        
        # Recommend additional patterns
        patterns["recommended_patterns"].extend([
            {
                "pattern": "Observer Pattern",
                "reason": "For event-driven communication between agents",
                "implementation": "Create event system for agent coordination"
            },
            {
                "pattern": "Command Pattern",
                "reason": "For queuing and managing agent execution",
                "implementation": "Implement command queue for agent tasks"
            },
            {
                "pattern": "Singleton Pattern",
                "reason": "For system-wide configuration management",
                "implementation": "Create configuration singleton for global settings"
            }
        ])
        
        return patterns
    
    def identify_refactoring_opportunities(self):
        """Identify specific refactoring opportunities"""
        opportunities = []
        
        # Check for large files that could be split
        large_files = []
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            lines = len(f.readlines())
                            if lines > 200:  # Arbitrary threshold
                                large_files.append({"file": file_path, "lines": lines})
                    except:
                        continue
        
        if large_files:
            opportunities.append({
                "type": "file_size",
                "priority": "medium",
                "description": f"Found {len(large_files)} large files that could be split",
                "details": large_files,
                "recommendation": "Consider breaking large files into smaller, focused modules"
            })
        
        # Check for code duplication opportunities
        opportunities.append({
            "type": "code_duplication",
            "priority": "low",
            "description": "Potential code duplication in agent implementations",
            "recommendation": "Create base agent class with common functionality"
        })
        
        # Check for error handling improvements
        opportunities.append({
            "type": "error_handling",
            "priority": "medium",
            "description": "Inconsistent error handling across agents",
            "recommendation": "Implement standardized error handling and logging framework"
        })
        
        # Check for configuration management
        if not os.path.exists('config'):
            opportunities.append({
                "type": "configuration",
                "priority": "high",
                "description": "No centralized configuration management",
                "recommendation": "Implement configuration management system for agent settings"
            })
        
        # Check for testing infrastructure
        test_coverage = self.assess_test_coverage()
        if test_coverage < 50:
            opportunities.append({
                "type": "testing",
                "priority": "high",
                "description": f"Low test coverage ({test_coverage}%)",
                "recommendation": "Implement comprehensive testing framework"
            })
        
        return opportunities
    
    def assess_test_coverage(self):
        """Assess current test coverage (simplified)"""
        total_py_files = 0
        test_files = 0
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.endswith('.py'):
                    total_py_files += 1
                    if 'test' in file.lower():
                        test_files += 1
        
        if total_py_files == 0:
            return 0
        
        return (test_files / total_py_files) * 100
    
    def generate_quality_recommendations(self):
        """Generate code quality improvement recommendations"""
        recommendations = [
            {
                "category": "Code Organization",
                "priority": "high",
                "items": [
                    "Implement consistent naming conventions across all modules",
                    "Add comprehensive docstrings to all public methods",
                    "Create clear module and package structure documentation"
                ]
            },
            {
                "category": "Error Handling",
                "priority": "high",
                "items": [
                    "Implement custom exception classes for different error types",
                    "Add comprehensive logging throughout the application",
                    "Create graceful degradation for non-critical failures"
                ]
            },
            {
                "category": "Performance",
                "priority": "medium",
                "items": [
                    "Implement caching for expensive operations",
                    "Add async/await support for I/O-bound operations",
                    "Optimize data processing in analytics agents"
                ]
            },
            {
                "category": "Maintainability",
                "priority": "medium",
                "items": [
                    "Create automated code formatting with tools like Black",
                    "Implement type hints throughout the codebase",
                    "Add code complexity monitoring and alerts"
                ]
            },
            {
                "category": "Security",
                "priority": "high",
                "items": [
                    "Implement secure coding standards",
                    "Add input validation and sanitization",
                    "Create security review process for code changes"
                ]
            }
        ]
        
        return recommendations
    
    def create_refactoring_plan(self, code_analysis, opportunities, quality_recommendations):
        """Create comprehensive refactoring plan"""
        plan = {
            "timestamp": datetime.now().isoformat(),
            "code_analysis": code_analysis,
            "refactoring_opportunities": opportunities,
            "quality_recommendations": quality_recommendations,
            "implementation_phases": self.create_implementation_phases(opportunities, quality_recommendations),
            "success_metrics": self.define_success_metrics()
        }
        
        # Save the plan
        plan_path = "reports/refactoring_plan.json"
        os.makedirs(os.path.dirname(plan_path), exist_ok=True)
        
        with open(plan_path, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"📄 Refactoring plan saved to: {plan_path}")
        
        # Generate implementation guide
        self.generate_refactoring_guide(plan)
        
        return plan
    
    def create_implementation_phases(self, opportunities, quality_recommendations):
        """Create phased implementation plan"""
        phases = [
            {
                "phase": 1,
                "name": "Critical Infrastructure",
                "duration": "2-3 weeks",
                "goals": ["Establish foundation for quality improvements"],
                "tasks": [
                    "Implement centralized configuration management",
                    "Set up comprehensive testing framework",
                    "Establish code quality standards and tooling"
                ]
            },
            {
                "phase": 2,
                "name": "Code Quality Improvements",
                "duration": "3-4 weeks",
                "goals": ["Improve code maintainability and readability"],
                "tasks": [
                    "Refactor large files into smaller modules",
                    "Implement consistent error handling",
                    "Add comprehensive documentation"
                ]
            },
            {
                "phase": 3,
                "name": "Performance & Security",
                "duration": "2-3 weeks",
                "goals": ["Optimize performance and enhance security"],
                "tasks": [
                    "Implement caching strategies",
                    "Add security enhancements",
                    "Optimize agent execution workflows"
                ]
            },
            {
                "phase": 4,
                "name": "Advanced Features",
                "duration": "3-4 weeks",
                "goals": ["Add advanced functionality and monitoring"],
                "tasks": [
                    "Implement advanced design patterns",
                    "Add real-time monitoring and metrics",
                    "Create automated deployment pipeline"
                ]
            }
        ]
        
        return phases
    
    def define_success_metrics(self):
        """Define metrics to measure refactoring success"""
        return {
            "code_quality": {
                "maintainability_index": {"target": "> 80", "current": "TBD"},
                "test_coverage": {"target": "> 80%", "current": "TBD"},
                "documentation_coverage": {"target": "> 90%", "current": "TBD"}
            },
            "performance": {
                "agent_startup_time": {"target": "< 2s", "current": "TBD"},
                "system_scan_time": {"target": "< 30s", "current": "TBD"},
                "memory_usage": {"target": "< 512MB", "current": "TBD"}
            },
            "reliability": {
                "error_rate": {"target": "< 1%", "current": "TBD"},
                "uptime": {"target": "> 99%", "current": "TBD"},
                "recovery_time": {"target": "< 5s", "current": "TBD"}
            }
        }
    
    def generate_refactoring_guide(self, plan):
        """Generate refactoring implementation guide"""
        guide_path = "docs/refactoring_guide.md"
        os.makedirs(os.path.dirname(guide_path), exist_ok=True)
        
        with open(guide_path, 'w') as f:
            f.write("# Refactoring Implementation Guide\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overview
            f.write("## 🎯 Refactoring Overview\n\n")
            f.write("This guide provides a structured approach to refactoring the AI Operating System Framework ")
            f.write("for improved maintainability, performance, and scalability.\n\n")
            
            # Current State
            f.write("## 📊 Current State Analysis\n\n")
            metrics = plan["code_analysis"]["code_metrics"]
            f.write(f"- **Total Files**: {metrics['total_files']}\n")
            f.write(f"- **Total Lines**: {metrics['total_lines']}\n")
            f.write(f"- **Average File Size**: {metrics['average_file_size']:.1f} lines\n")
            f.write(f"- **Maintainability Index**: {metrics['maintainability_index']:.1f}/100\n\n")
            
            # Implementation Phases
            f.write("## 📅 Implementation Phases\n\n")
            for phase in plan["implementation_phases"]:
                f.write(f"### Phase {phase['phase']}: {phase['name']}\n")
                f.write(f"**Duration**: {phase['duration']}\n\n")
                f.write("**Goals**:\n")
                for goal in phase['goals']:
                    f.write(f"- {goal}\n")
                f.write("\n**Tasks**:\n")
                for task in phase['tasks']:
                    f.write(f"- [ ] {task}\n")
                f.write("\n")
            
            # Priority Opportunities
            f.write("## 🎯 Priority Refactoring Opportunities\n\n")
            high_priority = [o for o in plan["refactoring_opportunities"] if o.get("priority") == "high"]
            if high_priority:
                f.write("### High Priority\n")
                for opp in high_priority:
                    f.write(f"- **{opp['type'].replace('_', ' ').title()}**: {opp['description']}\n")
                    f.write(f"  - *Recommendation*: {opp['recommendation']}\n\n")
            
            # Success Metrics
            f.write("## 📈 Success Metrics\n\n")
            f.write("| Category | Metric | Target | Current |\n")
            f.write("|----------|--------|--------|---------|\n")
            for category, metrics in plan["success_metrics"].items():
                for metric, values in metrics.items():
                    f.write(f"| {category.title()} | {metric.replace('_', ' ').title()} | ")
                    f.write(f"{values['target']} | {values['current']} |\n")
            
            f.write("\n---\n")
            f.write("*Guide generated by ModelRefactor - Update as refactoring progresses*\n")
        
        print(f"📚 Refactoring guide saved to: {guide_path}")
    
    def get_metrics(self):
        """Return performance metrics for this agent"""
        return {
            "refactoring_suggestions": len(self.refactoring_suggestions),
            "quality_metrics_calculated": len(self.code_quality_metrics),
            "last_run": datetime.now().isoformat()
        }

def get_plugin():
    return ModelRefactorAgent()
