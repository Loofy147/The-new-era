import asyncio
import json
import base64
import io
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import tempfile
import os
from pathlib import Path

from core.enhanced_plugin_interface import (
    EnhancedPluginInterface, PluginContext, ExecutionResult, ExecutionStatus,
    HealthCheckResult, HealthStatus, VoiceCapability, SelfHealingMixin
)

try:
    import speech_recognition as sr
    import pyttsx3
    import wave
    import pyaudio
    VOICE_DEPENDENCIES_AVAILABLE = True
except ImportError:
    VOICE_DEPENDENCIES_AVAILABLE = False

class VoiceAgent(EnhancedPluginInterface, VoiceCapability, SelfHealingMixin):
    """Advanced voice-enabled AI agent with speech processing capabilities"""
    
    def __init__(self):
        super().__init__(
            name="VoiceBot",
            role="Voice Interface Agent",
            description="AI agent that processes voice commands and provides voice responses with advanced speech recognition and synthesis"
        )
        
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        self.voice_models = {}
        self.conversation_history = []
        self.voice_commands = {}
        self.audio_buffer = []
        self.listening = False
        
        # Configuration
        self.wake_words = ["hey assistant", "voice bot", "ai assistant"]
        self.confidence_threshold = 0.7
        self.max_recording_duration = 30  # seconds
        self.voice_rate = 150  # words per minute
        self.voice_volume = 0.9
        
        # Voice processing metrics
        self.recognition_accuracy = 0.0
        self.response_time_ms = 0
        self.total_voice_interactions = 0
        self.successful_recognitions = 0
        
    async def initialize(self, context: PluginContext) -> bool:
        """Initialize the voice agent"""
        try:
            self.context = context
            self.log_info("Initializing Voice Agent...")
            
            if not VOICE_DEPENDENCIES_AVAILABLE:
                self.log_error("Voice dependencies not available. Install speech_recognition, pyttsx3, pyaudio")
                # Continue with limited functionality
                return True
            
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Initialize microphone
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.log_info("Microphone initialized and calibrated")
            except Exception as e:
                self.log_error(f"Microphone initialization failed: {e}")
                # Continue without microphone
            
            # Initialize text-to-speech
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', self.voice_rate)
                self.tts_engine.setProperty('volume', self.voice_volume)
                
                # Set voice if available
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Prefer female voice if available
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                
                self.log_info("Text-to-speech engine initialized")
            except Exception as e:
                self.log_error(f"TTS initialization failed: {e}")
            
            # Load voice commands
            await self._load_voice_commands()
            
            # Start background listening if enabled
            config = context.config.get('voice_agent', {})
            if config.get('background_listening', False):
                asyncio.create_task(self._background_listening())
            
            self._initialized = True
            self.log_info("Voice Agent initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(f"Voice Agent initialization failed: {e}")
            return False
    
    async def run(self) -> ExecutionResult:
        """Execute voice agent main functionality"""
        try:
            start_time = datetime.now()
            self.log_info("Running Voice Agent analysis...")
            
            results = {
                'voice_capabilities': await self._analyze_voice_capabilities(),
                'speech_recognition_test': await self._test_speech_recognition(),
                'voice_synthesis_test': await self._test_voice_synthesis(),
                'command_processing': await self._test_command_processing(),
                'conversation_analysis': await self._analyze_conversations(),
                'voice_metrics': await self._calculate_voice_metrics(),
                'recommendations': await self._generate_voice_recommendations()
            }
            
            # Generate comprehensive report
            report_path = await self._generate_voice_report(results)
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            self.log_info(f"Voice Agent analysis completed in {execution_time:.2f}ms")
            
            return {
                'status': 'success',
                'data': results,
                'execution_time_ms': int(execution_time),
                'metadata': {
                    'report_path': report_path,
                    'voice_capabilities_available': VOICE_DEPENDENCIES_AVAILABLE,
                    'total_voice_interactions': self.total_voice_interactions,
                    'recognition_accuracy': self.recognition_accuracy
                }
            }
            
        except Exception as e:
            self.log_error(f"Voice Agent execution failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'execution_time_ms': 0
            }
    
    async def health_check(self) -> HealthCheckResult:
        """Perform health check for voice agent"""
        try:
            details = {}
            
            # Check voice dependencies
            details['voice_dependencies'] = VOICE_DEPENDENCIES_AVAILABLE
            
            if VOICE_DEPENDENCIES_AVAILABLE:
                # Check speech recognition
                details['speech_recognition_available'] = self.recognizer is not None
                
                # Check microphone
                details['microphone_available'] = self.microphone is not None
                
                # Check TTS engine
                details['tts_engine_available'] = self.tts_engine is not None
                
                # Check recent performance
                details['recognition_accuracy'] = self.recognition_accuracy
                details['recent_interactions'] = self.total_voice_interactions
            
            # Determine overall health status
            if VOICE_DEPENDENCIES_AVAILABLE and self.recognizer and self.tts_engine:
                if self.recognition_accuracy >= 0.8:
                    status = HealthStatus.HEALTHY
                    message = "Voice agent is healthy with good recognition accuracy"
                elif self.recognition_accuracy >= 0.5:
                    status = HealthStatus.DEGRADED
                    message = "Voice agent is functional but recognition accuracy is degraded"
                else:
                    status = HealthStatus.DEGRADED
                    message = "Voice agent has low recognition accuracy"
            elif VOICE_DEPENDENCIES_AVAILABLE:
                status = HealthStatus.DEGRADED
                message = "Voice agent partially functional - some components missing"
            else:
                status = HealthStatus.DEGRADED
                message = "Voice dependencies not available - limited functionality"
            
            return HealthCheckResult(
                status=status,
                message=message,
                details=details
            )
            
        except Exception as e:
            return HealthCheckResult(
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {str(e)}",
                details={'error': str(e)}
            )
    
    def get_dependencies(self) -> List[str]:
        """Get list of dependencies"""
        return ['speech_recognition', 'pyttsx3', 'pyaudio', 'wave']
    
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Get configuration schema"""
        return {
            'background_listening': {
                'type': 'boolean',
                'default': False,
                'description': 'Enable background voice listening'
            },
            'wake_words': {
                'type': 'array',
                'default': ["hey assistant", "voice bot"],
                'description': 'Wake words to activate voice recognition'
            },
            'confidence_threshold': {
                'type': 'number',
                'default': 0.7,
                'description': 'Minimum confidence for speech recognition'
            },
            'voice_rate': {
                'type': 'integer',
                'default': 150,
                'description': 'Speech synthesis rate (words per minute)'
            },
            'voice_volume': {
                'type': 'number',
                'default': 0.9,
                'description': 'Speech synthesis volume (0.0 to 1.0)'
            }
        }
    
    # Voice Capability Implementation
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text"""
        if not VOICE_DEPENDENCIES_AVAILABLE or not self.recognizer:
            raise NotImplementedError("Speech recognition not available")
        
        try:
            # Convert bytes to audio data
            audio_file = io.BytesIO(audio_data)
            
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Perform recognition
            text = self.recognizer.recognize_google(audio)
            
            self.successful_recognitions += 1
            self.total_voice_interactions += 1
            
            # Update recognition accuracy
            self.recognition_accuracy = self.successful_recognitions / self.total_voice_interactions
            
            self.log_info(f"Speech recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            self.total_voice_interactions += 1
            self.recognition_accuracy = self.successful_recognitions / self.total_voice_interactions
            raise ValueError("Could not understand audio")
        except sr.RequestError as e:
            self.total_voice_interactions += 1
            self.recognition_accuracy = self.successful_recognitions / self.total_voice_interactions
            raise RuntimeError(f"Speech recognition service error: {e}")
    
    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech"""
        if not VOICE_DEPENDENCIES_AVAILABLE or not self.tts_engine:
            raise NotImplementedError("Text-to-speech not available")
        
        try:
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Configure TTS engine to save to file
            self.tts_engine.save_to_file(text, temp_path)
            self.tts_engine.runAndWait()
            
            # Read audio file as bytes
            with open(temp_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            self.log_info(f"Text synthesized to speech: {text[:50]}...")
            return audio_data
            
        except Exception as e:
            self.log_error(f"Text-to-speech failed: {e}")
            raise RuntimeError(f"Speech synthesis error: {e}")
    
    async def process_voice_command(self, command: str) -> ExecutionResult:
        """Process voice command"""
        try:
            start_time = datetime.now()
            command_lower = command.lower().strip()
            
            self.log_info(f"Processing voice command: {command}")
            
            # Add to conversation history
            self.conversation_history.append({
                'type': 'command',
                'content': command,
                'timestamp': start_time.isoformat()
            })
            
            response_text = ""
            command_executed = False
            
            # Check for built-in commands
            if any(wake_word in command_lower for wake_word in self.wake_words):
                response_text = "Hello! I'm listening. How can I help you?"
                command_executed = True
            
            elif "status" in command_lower or "health" in command_lower:
                health_result = await self.health_check()
                response_text = f"Voice agent status: {health_result.status.value}. {health_result.message}"
                command_executed = True
            
            elif "metrics" in command_lower or "statistics" in command_lower:
                metrics = await self._calculate_voice_metrics()
                response_text = f"Voice metrics: {metrics['total_interactions']} interactions, {metrics['recognition_accuracy']:.1%} accuracy"
                command_executed = True
            
            elif "time" in command_lower:
                current_time = datetime.now().strftime("%I:%M %p")
                response_text = f"The current time is {current_time}"
                command_executed = True
            
            elif "weather" in command_lower:
                response_text = "I'm sorry, I don't have access to weather information yet. This feature will be added in a future update."
                command_executed = True
            
            elif "help" in command_lower:
                response_text = "I can respond to commands like 'status', 'metrics', 'time', and general conversation. Try saying 'hey assistant' to get my attention."
                command_executed = True
            
            # Check custom voice commands
            if not command_executed:
                for pattern, response in self.voice_commands.items():
                    if pattern.lower() in command_lower:
                        response_text = response
                        command_executed = True
                        break
            
            # Default response for unrecognized commands
            if not command_executed:
                response_text = f"I heard you say: '{command}'. I'm still learning how to respond to that. Try asking for 'help' to see what I can do."
            
            # Add response to conversation history
            self.conversation_history.append({
                'type': 'response',
                'content': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            # Generate speech response if TTS is available
            audio_response = None
            if VOICE_DEPENDENCIES_AVAILABLE and self.tts_engine:
                try:
                    audio_response = await self.text_to_speech(response_text)
                except Exception as e:
                    self.log_error(f"Failed to generate audio response: {e}")
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.response_time_ms = execution_time
            
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                data={
                    'command': command,
                    'response_text': response_text,
                    'audio_response_available': audio_response is not None,
                    'command_recognized': command_executed,
                    'conversation_id': len(self.conversation_history) // 2
                },
                execution_time_ms=int(execution_time),
                metadata={
                    'audio_response_size_bytes': len(audio_response) if audio_response else 0
                }
            )
            
        except Exception as e:
            self.log_error(f"Voice command processing failed: {e}")
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                error=e
            )
    
    async def listen_for_command(self, timeout: int = 5) -> Optional[str]:
        """Listen for voice command from microphone"""
        if not VOICE_DEPENDENCIES_AVAILABLE or not self.recognizer or not self.microphone:
            raise NotImplementedError("Voice input not available")
        
        try:
            self.log_info(f"Listening for voice command (timeout: {timeout}s)...")
            
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=self.max_recording_duration)
            
            # Recognize speech
            command = self.recognizer.recognize_google(audio)
            self.log_info(f"Command received: {command}")
            
            return command
            
        except sr.WaitTimeoutError:
            self.log_info("Voice command timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            self.log_info("Could not understand the voice command")
            return None
        except Exception as e:
            self.log_error(f"Voice listening failed: {e}")
            return None
    
    async def _background_listening(self):
        """Background listening for wake words"""
        self.log_info("Starting background voice listening...")
        self.listening = True
        
        while self.listening:
            try:
                command = await self.listen_for_command(timeout=2)
                
                if command:
                    # Check for wake words
                    if any(wake_word in command.lower() for wake_word in self.wake_words):
                        self.log_info("Wake word detected, processing command...")
                        
                        # Process the command
                        result = await self.process_voice_command(command)
                        
                        # Speak the response if available
                        if result.data and result.data.get('response_text'):
                            await self._speak_response(result.data['response_text'])
                
                await asyncio.sleep(0.1)  # Brief pause between listening cycles
                
            except Exception as e:
                self.log_error(f"Background listening error: {e}")
                await asyncio.sleep(5)  # Wait before retrying
    
    async def _speak_response(self, text: str):
        """Speak a text response"""
        if VOICE_DEPENDENCIES_AVAILABLE and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                self.log_error(f"Failed to speak response: {e}")
    
    async def _load_voice_commands(self):
        """Load custom voice commands"""
        try:
            commands_file = Path("config/voice_commands.json")
            if commands_file.exists():
                with open(commands_file, 'r') as f:
                    self.voice_commands = json.load(f)
                self.log_info(f"Loaded {len(self.voice_commands)} custom voice commands")
            else:
                # Default commands
                self.voice_commands = {
                    "hello": "Hello! Nice to hear from you.",
                    "goodbye": "Goodbye! Have a great day!",
                    "thank you": "You're welcome!",
                    "how are you": "I'm doing well, thank you for asking!",
                    "what can you do": "I can process voice commands, answer questions, and help with various tasks through voice interaction."
                }
                self.log_info("Using default voice commands")
        except Exception as e:
            self.log_error(f"Failed to load voice commands: {e}")
            self.voice_commands = {}
    
    async def _analyze_voice_capabilities(self) -> Dict[str, Any]:
        """Analyze voice processing capabilities"""
        capabilities = {
            'speech_recognition_available': VOICE_DEPENDENCIES_AVAILABLE and self.recognizer is not None,
            'microphone_available': VOICE_DEPENDENCIES_AVAILABLE and self.microphone is not None,
            'text_to_speech_available': VOICE_DEPENDENCIES_AVAILABLE and self.tts_engine is not None,
            'background_listening_supported': True,
            'wake_word_detection': True,
            'custom_commands_supported': True,
            'conversation_history_tracking': True
        }
        
        if VOICE_DEPENDENCIES_AVAILABLE and self.tts_engine:
            try:
                voices = self.tts_engine.getProperty('voices')
                capabilities['available_voices'] = len(voices) if voices else 0
                capabilities['current_voice_rate'] = self.tts_engine.getProperty('rate')
                capabilities['current_voice_volume'] = self.tts_engine.getProperty('volume')
            except Exception as e:
                self.log_error(f"Failed to get TTS properties: {e}")
        
        return capabilities
    
    async def _test_speech_recognition(self) -> Dict[str, Any]:
        """Test speech recognition functionality"""
        test_results = {
            'recognition_engine_available': self.recognizer is not None,
            'microphone_available': self.microphone is not None,
            'total_recognitions_attempted': self.total_voice_interactions,
            'successful_recognitions': self.successful_recognitions,
            'current_accuracy': self.recognition_accuracy
        }
        
        if VOICE_DEPENDENCIES_AVAILABLE and self.recognizer:
            # Test with sample audio (if available)
            test_results['engine_version'] = "Google Speech Recognition"
            test_results['energy_threshold'] = self.recognizer.energy_threshold
            test_results['pause_threshold'] = self.recognizer.pause_threshold
        
        return test_results
    
    async def _test_voice_synthesis(self) -> Dict[str, Any]:
        """Test voice synthesis functionality"""
        test_results = {
            'tts_engine_available': self.tts_engine is not None,
            'synthesis_successful': False
        }
        
        if VOICE_DEPENDENCIES_AVAILABLE and self.tts_engine:
            try:
                # Test synthesis with a simple phrase
                test_phrase = "Voice synthesis test successful"
                audio_data = await self.text_to_speech(test_phrase)
                
                test_results['synthesis_successful'] = len(audio_data) > 0
                test_results['test_audio_size_bytes'] = len(audio_data)
                test_results['engine_name'] = self.tts_engine.getProperty('voice')
                
            except Exception as e:
                test_results['synthesis_error'] = str(e)
        
        return test_results
    
    async def _test_command_processing(self) -> Dict[str, Any]:
        """Test command processing functionality"""
        test_commands = [
            "hello",
            "status",
            "help",
            "what time is it"
        ]
        
        test_results = {
            'commands_tested': len(test_commands),
            'successful_processes': 0,
            'command_results': []
        }
        
        for command in test_commands:
            try:
                result = await self.process_voice_command(command)
                
                if result.status == ExecutionStatus.SUCCESS:
                    test_results['successful_processes'] += 1
                
                test_results['command_results'].append({
                    'command': command,
                    'status': result.status.value,
                    'response_available': bool(result.data and result.data.get('response_text'))
                })
                
            except Exception as e:
                test_results['command_results'].append({
                    'command': command,
                    'status': 'error',
                    'error': str(e)
                })
        
        test_results['processing_success_rate'] = test_results['successful_processes'] / len(test_commands)
        
        return test_results
    
    async def _analyze_conversations(self) -> Dict[str, Any]:
        """Analyze conversation history"""
        total_interactions = len(self.conversation_history)
        commands = [entry for entry in self.conversation_history if entry['type'] == 'command']
        responses = [entry for entry in self.conversation_history if entry['type'] == 'response']
        
        return {
            'total_interactions': total_interactions,
            'total_commands': len(commands),
            'total_responses': len(responses),
            'recent_interactions': self.conversation_history[-10:] if self.conversation_history else [],
            'conversation_balance': len(responses) / len(commands) if commands else 0,
            'most_recent_command': commands[-1]['content'] if commands else None,
            'most_recent_response': responses[-1]['content'] if responses else None
        }
    
    async def _calculate_voice_metrics(self) -> Dict[str, Any]:
        """Calculate voice processing metrics"""
        return {
            'total_interactions': self.total_voice_interactions,
            'successful_recognitions': self.successful_recognitions,
            'recognition_accuracy': self.recognition_accuracy,
            'average_response_time_ms': self.response_time_ms,
            'conversation_entries': len(self.conversation_history),
            'custom_commands_loaded': len(self.voice_commands),
            'wake_words_configured': len(self.wake_words)
        }
    
    async def _generate_voice_recommendations(self) -> List[Dict[str, Any]]:
        """Generate recommendations for voice processing improvements"""
        recommendations = []
        
        # Recognition accuracy recommendations
        if self.recognition_accuracy < 0.7:
            recommendations.append({
                'category': 'accuracy',
                'priority': 'high',
                'title': 'Improve Speech Recognition Accuracy',
                'description': f'Current accuracy is {self.recognition_accuracy:.1%}. Consider adjusting microphone settings or reducing background noise.',
                'action': 'Calibrate microphone and adjust energy threshold'
            })
        
        # Performance recommendations
        if self.response_time_ms > 2000:
            recommendations.append({
                'category': 'performance',
                'priority': 'medium',
                'title': 'Optimize Response Time',
                'description': f'Average response time is {self.response_time_ms:.0f}ms. Consider optimizing TTS processing.',
                'action': 'Optimize text-to-speech processing pipeline'
            })
        
        # Feature recommendations
        if not VOICE_DEPENDENCIES_AVAILABLE:
            recommendations.append({
                'category': 'setup',
                'priority': 'high',
                'title': 'Install Voice Dependencies',
                'description': 'Voice processing capabilities are limited without proper dependencies.',
                'action': 'Install speech_recognition, pyttsx3, and pyaudio packages'
            })
        
        # Usage recommendations
        if len(self.voice_commands) < 10:
            recommendations.append({
                'category': 'functionality',
                'priority': 'low',
                'title': 'Expand Voice Commands',
                'description': 'Add more custom voice commands to improve user experience.',
                'action': 'Create custom voice commands configuration file'
            })
        
        return recommendations
    
    async def _generate_voice_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive voice agent report"""
        report_content = f"""# Voice Agent Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent:** {self.name} ({self.role})

## Executive Summary

The Voice Agent provides advanced speech processing capabilities including:
- Speech-to-text recognition
- Text-to-speech synthesis  
- Voice command processing
- Conversation management

### Key Metrics
- **Total Voice Interactions:** {results['voice_metrics']['total_interactions']}
- **Recognition Accuracy:** {results['voice_metrics']['recognition_accuracy']:.1%}
- **Average Response Time:** {results['voice_metrics']['average_response_time_ms']:.0f}ms
- **Custom Commands:** {results['voice_metrics']['custom_commands_loaded']}

## Voice Capabilities Assessment

### Speech Recognition
- **Engine Available:** {results['voice_capabilities']['speech_recognition_available']}
- **Microphone Available:** {results['voice_capabilities']['microphone_available']}
- **Recognition Tests:** {results['speech_recognition_test']['current_accuracy']:.1%} accuracy

### Voice Synthesis  
- **TTS Engine Available:** {results['voice_capabilities']['text_to_speech_available']}
- **Synthesis Test:** {'Success' if results['voice_synthesis_test']['synthesis_successful'] else 'Failed'}
- **Available Voices:** {results['voice_capabilities'].get('available_voices', 'Unknown')}

### Command Processing
- **Commands Tested:** {results['command_processing']['commands_tested']}
- **Success Rate:** {results['command_processing']['processing_success_rate']:.1%}
- **Background Listening:** {results['voice_capabilities']['background_listening_supported']}

## Conversation Analysis

### Interaction Statistics
- **Total Conversations:** {results['conversation_analysis']['total_interactions']}
- **Commands Processed:** {results['conversation_analysis']['total_commands']}
- **Responses Generated:** {results['conversation_analysis']['total_responses']}

### Recent Activity
"""
        
        # Add recent interactions
        recent = results['conversation_analysis']['recent_interactions']
        if recent:
            report_content += "\nRecent Interactions:\n"
            for interaction in recent[-5:]:
                report_content += f"- {interaction['type'].title()}: {interaction['content'][:50]}...\n"
        
        # Add recommendations
        report_content += "\n## Recommendations\n\n"
        for rec in results['recommendations']:
            report_content += f"### {rec['title']} ({rec['priority'].upper()} priority)\n"
            report_content += f"**Category:** {rec['category']}\n"
            report_content += f"**Description:** {rec['description']}\n"
            report_content += f"**Action:** {rec['action']}\n\n"
        
        # Performance analysis
        report_content += f"""
## Performance Analysis

### Recognition Performance
- Current accuracy level: {results['voice_metrics']['recognition_accuracy']:.1%}
- Total attempts: {results['voice_metrics']['total_interactions']}
- Success rate trend: {'Improving' if results['voice_metrics']['recognition_accuracy'] > 0.8 else 'Needs attention'}

### Response Performance
- Average response time: {results['voice_metrics']['average_response_time_ms']:.0f}ms
- Performance rating: {'Excellent' if results['voice_metrics']['average_response_time_ms'] < 1000 else 'Good' if results['voice_metrics']['average_response_time_ms'] < 2000 else 'Needs optimization'}

## Technical Details

### Configuration
- Wake words: {len(results['voice_metrics']['wake_words_configured'])} configured
- Custom commands: {results['voice_metrics']['custom_commands_loaded']} loaded
- Voice rate: {results['voice_capabilities'].get('current_voice_rate', 'Unknown')} WPM
- Voice volume: {results['voice_capabilities'].get('current_voice_volume', 'Unknown')}

### System Health
- Overall status: {'Healthy' if results['voice_capabilities']['speech_recognition_available'] and results['voice_capabilities']['text_to_speech_available'] else 'Degraded'}
- Dependencies: {'All available' if results['voice_capabilities']['speech_recognition_available'] else 'Missing dependencies'}

---

*Report generated by Voice Agent - AI Operating System Framework*
"""
        
        # Save report
        os.makedirs("reports", exist_ok=True)
        report_path = f"reports/voice_agent_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        self.log_info(f"Voice agent report saved to: {report_path}")
        return report_path
    
    async def shutdown(self) -> bool:
        """Shutdown voice agent"""
        try:
            self.listening = False
            
            if self.tts_engine:
                try:
                    self.tts_engine.stop()
                except:
                    pass
            
            self.log_info("Voice Agent shutdown completed")
            return True
        except Exception as e:
            self.log_error(f"Error during shutdown: {e}")
            return False

def get_plugin():
    """Plugin entry point"""
    return VoiceAgent()
