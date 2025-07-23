import asyncio
import json
import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

# Import enhanced components
from core.enhanced_plugin_manager import EnhancedPluginManager
from core.enhanced_plugin_interface import PluginContext
from core.config_manager import ConfigurationManager, SystemConfig
from core.self_healing.healing_framework import SelfHealingFramework
from services.vector_search.vector_engine import VectorSearchEngine
from services.prompt_memory.enhanced_prompt_memory import EnhancedPromptMemoryService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/aios.log'),
        logging.StreamHandler()
    ]
)

class EnhancedAIOperatingSystem:
    """Enhanced AI Operating System with advanced features and professional architecture"""
    
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.config: SystemConfig = None
        self.plugin_manager: EnhancedPluginManager = None
        self.self_healing: SelfHealingFramework = None
        self.vector_search: VectorSearchEngine = None
        self.prompt_memory: EnhancedPromptMemoryService = None
        
        self.logger = logging.getLogger(__name__)
        self.manifest_path = "ai-agents-manifest.json"
        self.system_status = "initializing"
        
        # System metrics
        self.system_metrics = {
            'start_time': datetime.now(),
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_agents': 0,
            'healthy_agents': 0,
            'system_health_score': 0.0
        }
        
        # Create required directories
        self._create_directories()
    
    def _create_directories(self):
        """Create required system directories"""
        directories = [
            'logs', 'data', 'reports', 'config', 'cache',
            'data/vector_search', 'data/prompt_memory', 'data/self_healing'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    async def initialize(self) -> bool:
        """Initialize the enhanced AI Operating System"""
        try:
            self.logger.info("🚀 Initializing Enhanced AI Operating System Framework...")
            self.logger.info("="*80)
            
            # Load configuration
            await self._load_configuration()
            
            # Initialize self-healing framework
            await self._initialize_self_healing()
            
            # Initialize vector search engine
            await self._initialize_vector_search()
            
            # Initialize enhanced prompt memory
            await self._initialize_prompt_memory()
            
            # Initialize enhanced plugin manager
            await self._initialize_plugin_manager()
            
            # Load and update agent manifest
            await self._load_agent_manifest()
            
            # Perform system health check
            await self._perform_system_health_check()
            
            self.system_status = "ready"
            self.logger.info("✅ Enhanced AI Operating System initialized successfully")
            self.logger.info("="*80)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ System initialization failed: {e}")
            self.system_status = "failed"
            
            # Attempt self-healing
            if self.self_healing:
                await self.self_healing.register_failure("system", e, {
                    'component': 'system_initialization',
                    'error_type': 'initialization_failure'
                })
            
            return False
    
    async def _load_configuration(self):
        """Load system configuration"""
        try:
            self.config = self.config_manager.load_configuration()
            self.logger.info(f"📋 Configuration loaded - Environment: {self.config.environment}")
        except Exception as e:
            self.logger.error(f"Configuration loading failed: {e}")
            # Use default configuration
            self.config = SystemConfig()
    
    async def _initialize_self_healing(self):
        """Initialize self-healing framework"""
        try:
            self.self_healing = SelfHealingFramework()
            await self.self_healing.start_monitoring()
            self.logger.info("🔧 Self-healing framework initialized")
        except Exception as e:
            self.logger.error(f"Self-healing initialization failed: {e}")
    
    async def _initialize_vector_search(self):
        """Initialize vector search engine"""
        try:
            if self.config.vector_search_enabled:
                self.vector_search = VectorSearchEngine()
                self.logger.info("🔍 Vector search engine initialized")
            else:
                self.logger.info("⚪ Vector search disabled in configuration")
        except Exception as e:
            self.logger.error(f"Vector search initialization failed: {e}")
    
    async def _initialize_prompt_memory(self):
        """Initialize enhanced prompt memory service"""
        try:
            self.prompt_memory = EnhancedPromptMemoryService()
            self.logger.info("🧠 Enhanced prompt memory service initialized")
        except Exception as e:
            self.logger.error(f"Prompt memory initialization failed: {e}")
    
    async def _initialize_plugin_manager(self):
        """Initialize enhanced plugin manager"""
        try:
            self.plugin_manager = EnhancedPluginManager("plugins", self.config)
            
            # Create plugin context
            context = PluginContext(
                config=self.config.__dict__,
                logger=self.logger,
                metrics_collector=self,
                event_bus=self,
                storage=self,
                cache=self
            )
            
            # Initialize plugin manager
            success = await self.plugin_manager.initialize(context)
            if success:
                self.logger.info(f"🔌 Enhanced plugin manager initialized with {len(self.plugin_manager.plugins)} agents")
            else:
                self.logger.warning("⚠️ Plugin manager initialization had issues")
                
        except Exception as e:
            self.logger.error(f"Plugin manager initialization failed: {e}")
    
    async def _load_agent_manifest(self):
        """Load and update agent manifest"""
        try:
            manifest = {
                'system_info': {
                    'name': self.config.system_name,
                    'version': self.config.version,
                    'environment': self.config.environment,
                    'initialized_at': datetime.now().isoformat()
                },
                'capabilities': {
                    'vector_search': self.config.vector_search_enabled,
                    'self_healing': self.config.self_healing_enabled,
                    'voice_agents': self.config.voice_agents_enabled,
                    'multi_modal': self.config.multi_modal_enabled
                },
                'agents': []
            }
            
            # Add agent information
            if self.plugin_manager:
                for agent_name, agent in self.plugin_manager.plugins.items():
                    agent_info = {
                        'name': agent.name,
                        'role': agent.role,
                        'description': agent.description,
                        'dependencies': agent.get_dependencies(),
                        'capabilities': []
                    }
                    
                    # Check for special capabilities
                    if hasattr(agent, 'get_supported_modalities'):
                        agent_info['capabilities'].append('multi_modal')
                    if hasattr(agent, 'speech_to_text'):
                        agent_info['capabilities'].append('voice_processing')
                    if hasattr(agent, 'auto_recover'):
                        agent_info['capabilities'].append('self_healing')
                    
                    manifest['agents'].append(agent_info)
            
            # Save manifest
            with open(self.manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            self.logger.info(f"📋 Agent manifest updated with {len(manifest['agents'])} agents")
            
        except Exception as e:
            self.logger.error(f"Manifest loading failed: {e}")
    
    async def _perform_system_health_check(self):
        """Perform comprehensive system health check"""
        try:
            health_results = {}
            
            # Check each component
            if self.plugin_manager:
                plugin_health = await self.plugin_manager.get_system_metrics()
                health_results['plugin_manager'] = plugin_health
                self.system_metrics['total_agents'] = plugin_health['total_plugins']
                self.system_metrics['healthy_agents'] = plugin_health['healthy_plugins']
            
            if self.self_healing:
                healing_health = await self.self_healing.get_system_health_report()
                health_results['self_healing'] = healing_health
            
            if self.vector_search:
                vector_health = await self.vector_search.get_statistics()
                health_results['vector_search'] = vector_health
            
            if self.prompt_memory:
                memory_health = await self.prompt_memory.get_statistics()
                health_results['prompt_memory'] = memory_health
            
            # Calculate overall system health score
            self.system_metrics['system_health_score'] = self._calculate_health_score(health_results)
            
            self.logger.info(f"🏥 System health check completed - Score: {self.system_metrics['system_health_score']:.2f}/1.0")
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
    
    def _calculate_health_score(self, health_results: Dict[str, Any]) -> float:
        """Calculate overall system health score"""
        scores = []
        
        # Plugin manager health
        if 'plugin_manager' in health_results:
            pm_data = health_results['plugin_manager']
            if pm_data['total_plugins'] > 0:
                plugin_score = pm_data['healthy_plugins'] / pm_data['total_plugins']
                scores.append(plugin_score)
        
        # Self-healing health
        if 'self_healing' in health_results:
            sh_data = health_results['self_healing']
            if 'system_overview' in sh_data:
                recovery_rate = sh_data['system_overview'].get('recovery_success_rate', 0)
                scores.append(recovery_rate)
        
        # Vector search health
        if 'vector_search' in health_results:
            vs_data = health_results['vector_search']
            if vs_data.get('total_prompts', 0) > 0:
                scores.append(0.9)  # Assume healthy if running
            else:
                scores.append(0.7)  # Lower score if no data
        
        # Prompt memory health
        if 'prompt_memory' in health_results:
            pm_data = health_results['prompt_memory']
            if pm_data.get('vector_search', {}).get('total_prompts', 0) > 0:
                scores.append(0.9)
            else:
                scores.append(0.8)
        
        return sum(scores) / len(scores) if scores else 0.5
    
    async def run_agent(self, agent_name: str, timeout: Optional[int] = None) -> Dict[str, Any]:
        """Run a specific agent with enhanced error handling"""
        try:
            if not self.plugin_manager:
                raise RuntimeError("Plugin manager not initialized")
            
            self.logger.info(f"🔄 Running agent: {agent_name}")
            
            # Run agent with plugin manager
            result = await self.plugin_manager.run_plugin(agent_name, timeout)
            
            # Update metrics
            self.system_metrics['total_executions'] += 1
            if result.status.value == 'success':
                self.system_metrics['successful_executions'] += 1
            else:
                self.system_metrics['failed_executions'] += 1
            
            return {
                'agent': agent_name,
                'status': result.status.value,
                'execution_time_ms': result.execution_time_ms,
                'data': result.data,
                'metadata': result.metadata
            }
            
        except Exception as e:
            self.logger.error(f"❌ Agent {agent_name} execution failed: {e}")
            
            # Register failure with self-healing
            if self.self_healing:
                await self.self_healing.register_failure(agent_name, e, {
                    'execution_context': 'single_agent_run',
                    'agent': self.plugin_manager.plugins.get(agent_name) if self.plugin_manager else None
                })
            
            self.system_metrics['failed_executions'] += 1
            
            return {
                'agent': agent_name,
                'status': 'failed',
                'error': str(e),
                'execution_time_ms': 0
            }
    
    async def run_all_agents(self, parallel: bool = None) -> Dict[str, Any]:
        """Run all agents with enhanced orchestration"""
        try:
            if not self.plugin_manager:
                raise RuntimeError("Plugin manager not initialized")
            
            # Use configuration setting if not specified
            if parallel is None:
                parallel = self.config.max_concurrent_agents > 1
            
            self.logger.info(f"🚀 Running all agents ({'parallel' if parallel else 'sequential'} execution)")
            self.logger.info("="*60)
            
            start_time = datetime.now()
            
            # Run agents
            results = await self.plugin_manager.run_all_plugins(parallel=parallel)
            
            # Process results
            execution_summary = {
                'execution_mode': 'parallel' if parallel else 'sequential',
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_agents': len(results),
                'successful_agents': len([r for r in results.values() if r.status.value == 'success']),
                'failed_agents': len([r for r in results.values() if r.status.value == 'failed']),
                'agent_results': {}
            }
            
            # Convert results to serializable format
            for agent_name, result in results.items():
                execution_summary['agent_results'][agent_name] = {
                    'status': result.status.value,
                    'execution_time_ms': result.execution_time_ms,
                    'has_data': result.data is not None,
                    'metadata': result.metadata
                }
                
                # Update system metrics
                self.system_metrics['total_executions'] += 1
                if result.status.value == 'success':
                    self.system_metrics['successful_executions'] += 1
                else:
                    self.system_metrics['failed_executions'] += 1
            
            # Save execution summary
            await self._save_execution_summary(execution_summary)
            
            self.logger.info(f"📊 Execution Summary:")
            self.logger.info(f"   Total: {execution_summary['total_agents']}")
            self.logger.info(f"   Successful: {execution_summary['successful_agents']}")
            self.logger.info(f"   Failed: {execution_summary['failed_agents']}")
            self.logger.info(f"   Success Rate: {execution_summary['successful_agents']/execution_summary['total_agents']*100:.1f}%")
            
            return execution_summary
            
        except Exception as e:
            self.logger.error(f"❌ Full system execution failed: {e}")
            
            # Register system-level failure
            if self.self_healing:
                await self.self_healing.register_failure("system", e, {
                    'execution_context': 'full_system_run'
                })
            
            return {
                'status': 'system_failure',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def _save_execution_summary(self, summary: Dict[str, Any]):
        """Save execution summary to file"""
        try:
            summary_path = f"reports/execution_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            
            self.logger.info(f"📄 Execution summary saved to: {summary_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save execution summary: {e}")
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'system_status': self.system_status,
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': (datetime.now() - self.system_metrics['start_time']).total_seconds(),
            'configuration': {
                'environment': self.config.environment,
                'version': self.config.version,
                'debug': self.config.debug,
                'features': {
                    'vector_search': self.config.vector_search_enabled,
                    'self_healing': self.config.self_healing_enabled,
                    'voice_agents': self.config.voice_agents_enabled,
                    'multi_modal': self.config.multi_modal_enabled
                }
            },
            'metrics': self.system_metrics.copy(),
            'components': {}
        }
        
        # Add component status
        if self.plugin_manager:
            status['components']['plugin_manager'] = {
                'status': 'healthy',
                'total_agents': len(self.plugin_manager.plugins),
                'execution_order': self.plugin_manager.execution_order
            }
        
        if self.self_healing:
            healing_metrics = await self.self_healing.get_system_health_report()
            status['components']['self_healing'] = {
                'status': 'active',
                'total_failures': len(self.self_healing.failure_history),
                'total_recoveries': len(self.self_healing.recovery_history),
                'recovery_success_rate': healing_metrics['system_overview']['recovery_success_rate']
            }
        
        if self.vector_search:
            vector_stats = await self.vector_search.get_statistics()
            status['components']['vector_search'] = {
                'status': 'active',
                'total_prompts': vector_stats['total_prompts'],
                'embedding_dimension': vector_stats['embedding_dimension']
            }
        
        if self.prompt_memory:
            memory_stats = await self.prompt_memory.get_statistics()
            status['components']['prompt_memory'] = {
                'status': 'active',
                'total_conversations': memory_stats['conversations']['total_conversations'],
                'total_templates': memory_stats['templates']['total_templates']
            }
        
        # Calculate success rate
        if status['metrics']['total_executions'] > 0:
            status['metrics']['success_rate'] = status['metrics']['successful_executions'] / status['metrics']['total_executions']
        else:
            status['metrics']['success_rate'] = 0.0
        
        return status
    
    async def run_security_suite(self) -> Dict[str, Any]:
        """Run security-focused agents"""
        security_agents = ['SecuBot', 'ComplianceBot', 'PrivacyGuard']
        return await self._run_agent_suite("Security Suite", security_agents)
    
    async def run_analysis_suite(self) -> Dict[str, Any]:
        """Run analysis-focused agents"""
        analysis_agents = ['CostOptBot', 'InsightsBot', 'TestGenie', 'MultiModalBot']
        return await self._run_agent_suite("Analysis Suite", analysis_agents)
    
    async def run_creative_suite(self) -> Dict[str, Any]:
        """Run creative and design-focused agents"""
        creative_agents = ['BrainstormBot', 'ConvDesignBot', 'ArchitectureDesignerAgent']
        return await self._run_agent_suite("Creative Suite", creative_agents)
    
    async def run_voice_enabled_suite(self) -> Dict[str, Any]:
        """Run voice-enabled agents"""
        voice_agents = ['VoiceBot', 'MultiModalBot']
        return await self._run_agent_suite("Voice-Enabled Suite", voice_agents)
    
    async def _run_agent_suite(self, suite_name: str, agent_names: List[str]) -> Dict[str, Any]:
        """Run a specific suite of agents"""
        self.logger.info(f"🎯 Running {suite_name}...")
        self.logger.info("="*40)
        
        results = {}
        
        for agent_name in agent_names:
            if self.plugin_manager and agent_name in self.plugin_manager.plugins:
                result = await self.run_agent(agent_name)
                results[agent_name] = result
            else:
                self.logger.warning(f"⚠️ Agent {agent_name} not available")
                results[agent_name] = {
                    'status': 'not_available',
                    'message': f'Agent {agent_name} not found'
                }
        
        successful = len([r for r in results.values() if r.get('status') == 'success'])
        total = len(results)
        
        self.logger.info(f"📊 {suite_name} Results: {successful}/{total} successful")
        
        return {
            'suite_name': suite_name,
            'total_agents': total,
            'successful_agents': successful,
            'success_rate': successful / total if total > 0 else 0,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
    
    async def shutdown(self):
        """Graceful system shutdown"""
        try:
            self.logger.info("🔄 Initiating system shutdown...")
            
            # Shutdown components in reverse order
            if self.plugin_manager:
                await self.plugin_manager.shutdown()
                self.logger.info("✅ Plugin manager shutdown")
            
            if self.self_healing:
                await self.self_healing.shutdown()
                self.logger.info("✅ Self-healing framework shutdown")
            
            # Save final system metrics
            await self._save_final_metrics()
            
            self.system_status = "shutdown"
            self.logger.info("✅ Enhanced AI Operating System shutdown completed")
            
        except Exception as e:
            self.logger.error(f"❌ Error during shutdown: {e}")
    
    async def _save_final_metrics(self):
        """Save final system metrics"""
        try:
            final_metrics = {
                'session_summary': {
                    'start_time': self.system_metrics['start_time'].isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'total_uptime_seconds': (datetime.now() - self.system_metrics['start_time']).total_seconds(),
                    'system_health_score': self.system_metrics['system_health_score']
                },
                'execution_metrics': {
                    'total_executions': self.system_metrics['total_executions'],
                    'successful_executions': self.system_metrics['successful_executions'],
                    'failed_executions': self.system_metrics['failed_executions'],
                    'success_rate': self.system_metrics['successful_executions'] / max(1, self.system_metrics['total_executions'])
                },
                'agent_metrics': {
                    'total_agents': self.system_metrics['total_agents'],
                    'healthy_agents': self.system_metrics['healthy_agents']
                }
            }
            
            with open(f"reports/final_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                json.dump(final_metrics, f, indent=2)
            
        except Exception as e:
            self.logger.error(f"Failed to save final metrics: {e}")
    
    # Event bus implementation (simplified)
    def emit(self, event_type: str, data: Dict[str, Any]):
        """Emit event to system event bus"""
        self.logger.debug(f"Event emitted: {event_type}")
    
    # Storage interface (simplified)
    def store(self, key: str, data: Any):
        """Store data in system storage"""
        pass
    
    def retrieve(self, key: str) -> Any:
        """Retrieve data from system storage"""
        return None

async def main():
    """Main entry point for the Enhanced AI Operating System"""
    # Initialize system
    ai_os = EnhancedAIOperatingSystem()
    
    try:
        # Initialize the system
        success = await ai_os.initialize()
        
        if not success:
            print("❌ System initialization failed")
            return
        
        # Show system status
        status = await ai_os.get_system_status()
        print(f"\n🖥️ System Status: {status['system_status']}")
        print(f"🏥 Health Score: {status['metrics']['system_health_score']:.2f}")
        print(f"🤖 Total Agents: {status['metrics']['total_agents']}")
        
        # Run demonstration based on configuration
        if ai_os.config.environment == "demo":
            print("\n🎮 Running demonstration mode...")
            
            # Run creative suite
            await ai_os.run_creative_suite()
            
            # Run voice-enabled suite if enabled
            if ai_os.config.voice_agents_enabled:
                await ai_os.run_voice_enabled_suite()
            
            # Run full system
            await ai_os.run_all_agents(parallel=True)
            
        else:
            print("\n🚀 Running full system analysis...")
            # Run all agents
            results = await ai_os.run_all_agents()
            
            # Show final status
            final_status = await ai_os.get_system_status()
            print(f"\n📊 Final Results:")
            print(f"   Executions: {final_status['metrics']['total_executions']}")
            print(f"   Success Rate: {final_status['metrics']['success_rate']:.1%}")
            print(f"   Health Score: {final_status['metrics']['system_health_score']:.2f}")
    
    except KeyboardInterrupt:
        print("\n⏹️ Received interrupt signal")
    except Exception as e:
        print(f"❌ System error: {e}")
    finally:
        # Graceful shutdown
        await ai_os.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
