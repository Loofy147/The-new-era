from core.plugin_manager import PluginManager
import json
import os
from datetime import datetime

class AIOperatingSystem:
    def __init__(self):
        self.plugin_manager = PluginManager("plugins")
        self.agents = {}
        self.manifest_path = "ai-agents-manifest.json"

    def initialize(self):
        """Initialize the AI Operating System"""
        print("🚀 Initializing AI Operating System Framework...")
        print("="*60)

        # Load agent manifest
        self.load_agent_manifest()

        # Discover and load plugins
        self.plugin_manager.discover_plugins()

        # Register discovered agents
        self.register_agents()

        print(f"✅ System initialized with {len(self.agents)} agents")
        print("="*60)

    def load_agent_manifest(self):
        """Load the agent manifest file"""
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                print(f"📋 Loaded manifest with {len(manifest.get('agents', []))} agent definitions")
        else:
            print("⚠️ Agent manifest not found")

    def register_agents(self):
        """Register all discovered agents"""
        for plugin in self.plugin_manager.plugins:
            if hasattr(plugin, 'name') and hasattr(plugin, 'role'):
                self.agents[plugin.name] = plugin
                print(f"  ✅ Registered {plugin.name} ({plugin.role})")

    def list_agents(self):
        """List all available agents"""
        print("\n🤖 Available AI Agents:")
        print("-"*60)

        for name, agent in self.agents.items():
            print(f"📋 {name}")
            print(f"   Role: {agent.role}")
            print(f"   Description: {agent.description}")
            print()

    def run_agent(self, agent_name):
        """Run a specific agent"""
        if agent_name in self.agents:
            print(f"\n🔄 Running {agent_name}...")
            print("-"*40)
            result = self.agents[agent_name].run()
            print(f"✅ {agent_name} completed successfully")
            return result
        else:
            print(f"❌ Agent '{agent_name}' not found")
            return None

    def run_all_agents(self):
        """Run all agents in sequence"""
        print("\n🔄 Running all agents...")
        print("="*60)

        results = {}
        for name, agent in self.agents.items():
            try:
                print(f"\n▶️ Starting {name}...")
                result = agent.run()
                results[name] = {
                    "status": "success",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
                print(f"✅ {name} completed")
            except Exception as e:
                print(f"❌ {name} failed: {e}")
                results[name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }

        # Save execution summary
        self.save_execution_summary(results)

        print("\n📊 Execution Summary:")
        successful = len([r for r in results.values() if r["status"] == "success"])
        failed = len([r for r in results.values() if r["status"] == "error"])
        print(f"   Successful: {successful}/{len(results)}")
        print(f"   Failed: {failed}/{len(results)}")

        return results

    def run_security_suite(self):
        """Run security-focused agents"""
        security_agents = ['SecuBot', 'ComplianceBot', 'PrivacyGuard']
        print("\n🔒 Running Security Suite...")
        print("="*40)

        results = {}
        for agent_name in security_agents:
            if agent_name in self.agents:
                results[agent_name] = self.run_agent(agent_name)

        return results

    def run_analysis_suite(self):
        """Run analysis-focused agents"""
        analysis_agents = ['CostOptBot', 'InsightsBot', 'TestGenie']
        print("\n📊 Running Analysis Suite...")
        print("="*40)

        results = {}
        for agent_name in analysis_agents:
            if agent_name in self.agents:
                results[agent_name] = self.run_agent(agent_name)

        return results

    def save_execution_summary(self, results):
        """Save execution summary to file"""
        summary_path = "reports/execution_summary.json"
        os.makedirs(os.path.dirname(summary_path), exist_ok=True)

        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(results),
            "successful_agents": len([r for r in results.values() if r["status"] == "success"]),
            "failed_agents": len([r for r in results.values() if r["status"] == "error"]),
            "execution_details": results
        }

        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"📄 Execution summary saved to: {summary_path}")

    def show_system_status(self):
        """Show comprehensive system status"""
        print("\n🖥️ AI Operating System Status")
        print("="*60)

        # System info
        print(f"📊 Total Agents: {len(self.agents)}")
        print(f"📁 Plugin Directory: plugins/")
        print(f"📋 Manifest File: {self.manifest_path}")

        # Check reports directory
        if os.path.exists('reports'):
            report_files = [f for f in os.listdir('reports') if f.endswith('.json')]
            print(f"📄 Available Reports: {len(report_files)}")
        else:
            print("📄 No reports generated yet")

        # Agent health check
        print("\n🏥 Agent Health Check:")
        for name, agent in self.agents.items():
            try:
                # Check if agent has required methods
                has_run = hasattr(agent, 'run')
                has_metrics = hasattr(agent, 'get_metrics')

                status = "🟢" if has_run and has_metrics else "🟡" if has_run else "🔴"
                print(f"   {status} {name}: {'Healthy' if has_run and has_metrics else 'Partial' if has_run else 'Unhealthy'}")
            except Exception as e:
                print(f"   🔴 {name}: Error - {e}")

def main():
    """Main entry point for the AI Operating System"""
    ai_os = AIOperatingSystem()
    ai_os.initialize()

    # Show available options
    print("\n🎯 Available Commands:")
    print("   1. List all agents")
    print("   2. Run all agents")
    print("   3. Run security suite")
    print("   4. Run analysis suite")
    print("   5. Show system status")
    print("   6. Run specific agent")

    # For automated execution, run all agents by default
    print("\n🚀 Running full system analysis...")
    ai_os.run_all_agents()

    # Show final status
    ai_os.show_system_status()

if __name__ == "__main__":
    main()
