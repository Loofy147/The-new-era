from core.plugin_interface import PluginInterface
import json
import os
from datetime import datetime, timedelta
import glob

class AnalyticsInsightsAgent(PluginInterface):
    def __init__(self):
        self.name = "InsightsBot"
        self.role = "Analytics & Insights Agent"
        self.description = "Gathers system KPIs, produces insights from data patterns"
        self.metrics_history = []
        self.insights_generated = []
    
    def run(self):
        print(f"🤖 {self.name} ({self.role}) is generating insights...")
        
        # Collect system metrics
        system_metrics = self.collect_system_metrics()
        
        # Analyze agent performance
        agent_insights = self.analyze_agent_performance()
        
        # Generate usage patterns
        usage_patterns = self.analyze_usage_patterns()
        
        # Create comprehensive insights report
        insights_report = self.generate_insights_report(system_metrics, agent_insights, usage_patterns)
        
        print(f"✅ {self.name} completed analytics and insights generation")
        return insights_report
    
    def collect_system_metrics(self):
        """Collect various system performance metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system_health": self.assess_system_health(),
            "file_metrics": self.analyze_file_metrics(),
            "plugin_metrics": self.analyze_plugin_metrics(),
            "service_metrics": self.analyze_service_metrics()
        }
        
        print(f"📊 Collected system metrics")
        return metrics
    
    def assess_system_health(self):
        """Assess overall system health"""
        health_score = 100
        issues = []
        
        # Check for critical directories
        required_dirs = ['core', 'plugins', 'services']
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                health_score -= 20
                issues.append(f"Missing required directory: {dir_name}")
        
        # Check for essential files
        essential_files = ['main.py', 'ai-agents-manifest.json', 'requirements.txt']
        for file_name in essential_files:
            if not os.path.exists(file_name):
                health_score -= 10
                issues.append(f"Missing essential file: {file_name}")
        
        # Check reports directory (created by other agents)
        if os.path.exists('reports'):
            report_files = len([f for f in os.listdir('reports') if f.endswith('.json')])
            if report_files > 0:
                health_score += 5  # Bonus for active reporting
        
        return {
            "score": max(0, health_score),
            "status": "healthy" if health_score >= 80 else "warning" if health_score >= 60 else "critical",
            "issues": issues,
            "last_check": datetime.now().isoformat()
        }
    
    def analyze_file_metrics(self):
        """Analyze file system metrics"""
        metrics = {
            "total_files": 0,
            "python_files": 0,
            "documentation_files": 0,
            "configuration_files": 0,
            "largest_files": [],
            "newest_files": []
        }
        
        file_info = []
        
        # Walk through directory structure
        for root, dirs, files in os.walk('.'):
            # Skip hidden and virtual environment directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    stat_info = os.stat(file_path)
                    file_info.append({
                        'path': file_path,
                        'size': stat_info.st_size,
                        'modified': stat_info.st_mtime,
                        'extension': os.path.splitext(file)[1]
                    })
                    
                    metrics["total_files"] += 1
                    
                    if file.endswith('.py'):
                        metrics["python_files"] += 1
                    elif file.endswith(('.md', '.txt', '.rst')):
                        metrics["documentation_files"] += 1
                    elif file.endswith(('.json', '.yaml', '.yml', '.ini', '.cfg')):
                        metrics["configuration_files"] += 1
                        
                except OSError:
                    continue
        
        # Find largest files
        file_info.sort(key=lambda x: x['size'], reverse=True)
        metrics["largest_files"] = [
            {"path": f['path'], "size_kb": f['size'] // 1024}
            for f in file_info[:5]
        ]
        
        # Find newest files
        file_info.sort(key=lambda x: x['modified'], reverse=True)
        metrics["newest_files"] = [
            {
                "path": f['path'], 
                "modified": datetime.fromtimestamp(f['modified']).isoformat()
            }
            for f in file_info[:5]
        ]
        
        return metrics
    
    def analyze_plugin_metrics(self):
        """Analyze plugin system metrics"""
        metrics = {
            "total_plugins": 0,
            "plugin_types": {},
            "plugin_complexity": {},
            "plugin_health": []
        }
        
        # Count plugins
        if os.path.exists('plugins'):
            plugin_dirs = [d for d in os.listdir('plugins') if os.path.isdir(os.path.join('plugins', d))]
            metrics["total_plugins"] = len(plugin_dirs)
            
            for plugin_dir in plugin_dirs:
                plugin_path = os.path.join('plugins', plugin_dir, '__init__.py')
                if os.path.exists(plugin_path):
                    # Analyze plugin complexity
                    with open(plugin_path, 'r') as f:
                        content = f.read()
                        lines = len(content.split('\n'))
                        classes = content.count('class ')
                        functions = content.count('def ')
                        
                        metrics["plugin_complexity"][plugin_dir] = {
                            "lines_of_code": lines,
                            "classes": classes,
                            "functions": functions,
                            "complexity_score": (lines // 10) + classes + functions
                        }
                        
                        # Determine plugin type from role
                        if "Agent" in content:
                            plugin_type = "agent"
                        elif "Service" in content:
                            plugin_type = "service"
                        else:
                            plugin_type = "utility"
                        
                        metrics["plugin_types"][plugin_type] = metrics["plugin_types"].get(plugin_type, 0) + 1
                        
                        # Assess plugin health
                        health_score = 100
                        issues = []
                        
                        if 'def run(' not in content:
                            health_score -= 50
                            issues.append("Missing run method")
                        
                        if 'get_plugin()' not in content:
                            health_score -= 30
                            issues.append("Missing get_plugin function")
                        
                        if len(content) < 100:
                            health_score -= 20
                            issues.append("Plugin appears incomplete")
                        
                        metrics["plugin_health"].append({
                            "plugin": plugin_dir,
                            "health_score": health_score,
                            "issues": issues
                        })
        
        return metrics
    
    def analyze_service_metrics(self):
        """Analyze service metrics"""
        metrics = {
            "services_count": 0,
            "service_health": [],
            "api_endpoints": 0
        }
        
        # Check services directory
        if os.path.exists('services'):
            service_dirs = [d for d in os.listdir('services') if os.path.isdir(os.path.join('services', d))]
            metrics["services_count"] = len(service_dirs)
            
            for service_dir in service_dirs:
                service_path = os.path.join('services', service_dir)
                health_score = 100
                issues = []
                endpoints = 0
                
                # Check for app.py
                app_py_path = os.path.join(service_path, 'app.py')
                if os.path.exists(app_py_path):
                    with open(app_py_path, 'r') as f:
                        content = f.read()
                        endpoints = content.count('@app.route')
                        
                        if 'Flask' not in content:
                            health_score -= 20
                            issues.append("Not using Flask framework")
                        
                        if endpoints == 0:
                            health_score -= 30
                            issues.append("No API endpoints found")
                else:
                    health_score -= 50
                    issues.append("Missing app.py file")
                
                metrics["service_health"].append({
                    "service": service_dir,
                    "health_score": health_score,
                    "endpoints": endpoints,
                    "issues": issues
                })
                
                metrics["api_endpoints"] += endpoints
        
        return metrics
    
    def analyze_agent_performance(self):
        """Analyze performance of different agents"""
        insights = {
            "agent_activity": {},
            "report_generation": {},
            "recommendations": []
        }
        
        # Analyze reports generated by agents
        if os.path.exists('reports'):
            report_files = glob.glob('reports/*.json')
            
            for report_file in report_files:
                try:
                    with open(report_file, 'r') as f:
                        report_data = json.load(f)
                        
                        # Extract timestamp
                        timestamp = report_data.get('timestamp', 'unknown')
                        report_type = os.path.basename(report_file).replace('.json', '')
                        
                        insights["report_generation"][report_type] = {
                            "last_generated": timestamp,
                            "file_size": os.path.getsize(report_file),
                            "data_points": len(str(report_data))
                        }
                        
                        # Analyze specific report types
                        if 'security_score' in report_data:
                            score = report_data['security_score']
                            if score < 70:
                                insights["recommendations"].append({
                                    "type": "security",
                                    "priority": "high",
                                    "message": f"Security score ({score}) below recommended threshold"
                                })
                        
                        if 'privacy_score' in report_data:
                            score = report_data['privacy_score']
                            if score < 80:
                                insights["recommendations"].append({
                                    "type": "privacy",
                                    "priority": "high",
                                    "message": f"Privacy score ({score}) needs improvement"
                                })
                        
                        if 'total_potential_savings' in report_data:
                            savings = report_data['total_potential_savings']
                            if savings > 500:
                                insights["recommendations"].append({
                                    "type": "cost",
                                    "priority": "medium",
                                    "message": f"Significant cost savings (${savings}) identified"
                                })
                
                except Exception as e:
                    print(f"Error analyzing report {report_file}: {e}")
        
        return insights
    
    def analyze_usage_patterns(self):
        """Analyze system usage patterns"""
        patterns = {
            "development_activity": self.assess_development_activity(),
            "file_changes": self.analyze_file_changes(),
            "growth_trends": self.calculate_growth_trends()
        }
        
        return patterns
    
    def assess_development_activity(self):
        """Assess recent development activity"""
        activity = {
            "recent_files_created": 0,
            "recent_files_modified": 0,
            "most_active_directories": []
        }
        
        # Look for recently created/modified files
        now = datetime.now().timestamp()
        week_ago = now - (7 * 24 * 3600)  # 7 days ago
        
        dir_activity = {}
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    stat_info = os.stat(file_path)
                    
                    if stat_info.st_ctime > week_ago:
                        activity["recent_files_created"] += 1
                    
                    if stat_info.st_mtime > week_ago:
                        activity["recent_files_modified"] += 1
                        
                        # Track directory activity
                        dir_name = os.path.dirname(file_path)
                        dir_activity[dir_name] = dir_activity.get(dir_name, 0) + 1
                        
                except OSError:
                    continue
        
        # Sort directories by activity
        sorted_dirs = sorted(dir_activity.items(), key=lambda x: x[1], reverse=True)
        activity["most_active_directories"] = [
            {"directory": dir_name, "changes": count}
            for dir_name, count in sorted_dirs[:5]
        ]
        
        return activity
    
    def analyze_file_changes(self):
        """Analyze patterns in file changes"""
        changes = {
            "file_types_modified": {},
            "size_distribution": {"small": 0, "medium": 0, "large": 0}
        }
        
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                extension = os.path.splitext(file)[1] or 'no_extension'
                
                try:
                    size = os.path.getsize(file_path)
                    
                    # Track file type modifications
                    changes["file_types_modified"][extension] = changes["file_types_modified"].get(extension, 0) + 1
                    
                    # Categorize by size
                    if size < 1024:  # < 1KB
                        changes["size_distribution"]["small"] += 1
                    elif size < 10240:  # < 10KB
                        changes["size_distribution"]["medium"] += 1
                    else:  # >= 10KB
                        changes["size_distribution"]["large"] += 1
                        
                except OSError:
                    continue
        
        return changes
    
    def calculate_growth_trends(self):
        """Calculate system growth trends"""
        trends = {
            "project_maturity": "developing",
            "complexity_trend": "increasing",
            "recommendations": []
        }
        
        # Simple heuristics for project maturity
        total_files = sum(1 for _ in glob.glob('**/*', recursive=True) if os.path.isfile(_))
        python_files = len(glob.glob('**/*.py', recursive=True))
        
        if total_files > 50 and python_files > 10:
            trends["project_maturity"] = "mature"
        elif total_files > 20 and python_files > 5:
            trends["project_maturity"] = "growing"
        
        # Recommendations based on analysis
        if python_files > 20:
            trends["recommendations"].append("Consider implementing automated testing")
        
        if not os.path.exists('docs'):
            trends["recommendations"].append("Create comprehensive documentation")
        
        if not os.path.exists('tests'):
            trends["recommendations"].append("Implement test suite")
        
        return trends
    
    def generate_insights_report(self, system_metrics, agent_insights, usage_patterns):
        """Generate comprehensive insights report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "executive_summary": self.generate_executive_summary(system_metrics, agent_insights),
            "system_metrics": system_metrics,
            "agent_insights": agent_insights,
            "usage_patterns": usage_patterns,
            "key_insights": self.extract_key_insights(system_metrics, agent_insights, usage_patterns),
            "recommendations": self.generate_recommendations(system_metrics, agent_insights, usage_patterns)
        }
        
        # Save report
        report_path = "reports/insights_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Insights report saved to: {report_path}")
        
        # Generate executive dashboard
        self.generate_executive_dashboard(report)
        
        return report
    
    def generate_executive_summary(self, system_metrics, agent_insights):
        """Generate executive summary of key findings"""
        summary = {
            "overall_health": system_metrics["system_health"]["status"],
            "total_agents": system_metrics["plugin_metrics"]["total_plugins"],
            "active_services": system_metrics["service_metrics"]["services_count"],
            "recent_activity": len(agent_insights["report_generation"]),
            "key_concerns": []
        }
        
        # Identify key concerns
        if system_metrics["system_health"]["score"] < 80:
            summary["key_concerns"].append("System health below optimal")
        
        if len(agent_insights["recommendations"]) > 0:
            high_priority = [r for r in agent_insights["recommendations"] if r["priority"] == "high"]
            if high_priority:
                summary["key_concerns"].append(f"{len(high_priority)} high-priority issues identified")
        
        return summary
    
    def extract_key_insights(self, system_metrics, agent_insights, usage_patterns):
        """Extract key insights from the analysis"""
        insights = []
        
        # Plugin insights
        total_plugins = system_metrics["plugin_metrics"]["total_plugins"]
        if total_plugins > 5:
            insights.append({
                "category": "Architecture",
                "insight": f"System has {total_plugins} plugins, indicating good modularity",
                "impact": "positive"
            })
        
        # Development activity insights
        recent_changes = usage_patterns["development_activity"]["recent_files_modified"]
        if recent_changes > 10:
            insights.append({
                "category": "Development",
                "insight": f"{recent_changes} files modified recently, showing active development",
                "impact": "positive"
            })
        
        # Service insights
        api_endpoints = system_metrics["service_metrics"]["api_endpoints"]
        if api_endpoints > 0:
            insights.append({
                "category": "Services",
                "insight": f"System provides {api_endpoints} API endpoints for external integration",
                "impact": "positive"
            })
        
        # Security insights
        security_reports = len([r for r in agent_insights["report_generation"] if 'security' in r])
        if security_reports > 0:
            insights.append({
                "category": "Security",
                "insight": "Active security monitoring with automated reporting",
                "impact": "positive"
            })
        
        return insights
    
    def generate_recommendations(self, system_metrics, agent_insights, usage_patterns):
        """Generate actionable recommendations"""
        recommendations = []
        
        # System health recommendations
        if system_metrics["system_health"]["score"] < 80:
            recommendations.append({
                "category": "System Health",
                "priority": "high",
                "action": "Address system health issues",
                "details": system_metrics["system_health"]["issues"]
            })
        
        # Plugin recommendations
        unhealthy_plugins = [p for p in system_metrics["plugin_metrics"]["plugin_health"] if p["health_score"] < 80]
        if unhealthy_plugins:
            recommendations.append({
                "category": "Plugin Quality",
                "priority": "medium",
                "action": f"Improve {len(unhealthy_plugins)} plugins with health issues",
                "details": [p["plugin"] for p in unhealthy_plugins]
            })
        
        # Documentation recommendations
        doc_files = system_metrics["file_metrics"]["documentation_files"]
        total_files = system_metrics["file_metrics"]["total_files"]
        if doc_files / max(total_files, 1) < 0.1:  # Less than 10% documentation
            recommendations.append({
                "category": "Documentation",
                "priority": "medium",
                "action": "Increase documentation coverage",
                "details": f"Only {doc_files} documentation files for {total_files} total files"
            })
        
        # Add agent-specific recommendations
        recommendations.extend(agent_insights["recommendations"])
        
        return recommendations
    
    def generate_executive_dashboard(self, report):
        """Generate executive dashboard in markdown format"""
        dashboard_path = "reports/executive_dashboard.md"
        
        with open(dashboard_path, 'w') as f:
            f.write("# Executive Dashboard\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Executive Summary
            summary = report["executive_summary"]
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **System Health**: {summary['overall_health'].upper()}\n")
            f.write(f"- **Active Agents**: {summary['total_agents']}\n")
            f.write(f"- **Services Running**: {summary['active_services']}\n")
            f.write(f"- **Recent Reports**: {summary['recent_activity']}\n\n")
            
            if summary["key_concerns"]:
                f.write("### 🚨 Key Concerns\n")
                for concern in summary["key_concerns"]:
                    f.write(f"- {concern}\n")
                f.write("\n")
            
            # Key Metrics
            f.write("## 📈 Key Metrics\n\n")
            f.write("| Metric | Value | Status |\n")
            f.write("|--------|-------|--------|\n")
            
            health_score = report["system_metrics"]["system_health"]["score"]
            health_status = "🟢" if health_score >= 80 else "🟡" if health_score >= 60 else "🔴"
            f.write(f"| System Health Score | {health_score}/100 | {health_status} |\n")
            
            total_files = report["system_metrics"]["file_metrics"]["total_files"]
            f.write(f"| Total Files | {total_files} | 📁 |\n")
            
            python_files = report["system_metrics"]["file_metrics"]["python_files"]
            f.write(f"| Python Files | {python_files} | 🐍 |\n")
            
            api_endpoints = report["system_metrics"]["service_metrics"]["api_endpoints"]
            f.write(f"| API Endpoints | {api_endpoints} | 🔗 |\n")
            
            f.write("\n")
            
            # Key Insights
            f.write("## 💡 Key Insights\n\n")
            for insight in report["key_insights"]:
                impact_emoji = "✅" if insight["impact"] == "positive" else "⚠️"
                f.write(f"- {impact_emoji} **{insight['category']}**: {insight['insight']}\n")
            f.write("\n")
            
            # Recommendations
            f.write("## 🎯 Priority Recommendations\n\n")
            high_priority = [r for r in report["recommendations"] if r.get("priority") == "high"]
            medium_priority = [r for r in report["recommendations"] if r.get("priority") == "medium"]
            
            if high_priority:
                f.write("### High Priority\n")
                for rec in high_priority:
                    f.write(f"- 🔴 **{rec['category']}**: {rec['action']}\n")
                f.write("\n")
            
            if medium_priority:
                f.write("### Medium Priority\n")
                for rec in medium_priority:
                    f.write(f"- 🟡 **{rec['category']}**: {rec['action']}\n")
                f.write("\n")
            
            # Recent Activity
            f.write("## 🔄 Recent Activity\n\n")
            activity = report["usage_patterns"]["development_activity"]
            f.write(f"- Files created this week: {activity['recent_files_created']}\n")
            f.write(f"- Files modified this week: {activity['recent_files_modified']}\n")
            
            if activity["most_active_directories"]:
                f.write("\n### Most Active Directories\n")
                for dir_info in activity["most_active_directories"]:
                    f.write(f"- {dir_info['directory']}: {dir_info['changes']} changes\n")
            
            f.write("\n---\n")
            f.write("*Dashboard generated by InsightsBot - Run regularly for updated metrics*\n")
        
        print(f"📊 Executive dashboard saved to: {dashboard_path}")
    
    def get_metrics(self):
        """Return performance metrics for this agent"""
        return {
            "insights_generated": len(self.insights_generated),
            "metrics_collected": len(self.metrics_history),
            "last_run": datetime.now().isoformat()
        }

def get_plugin():
    return AnalyticsInsightsAgent()
