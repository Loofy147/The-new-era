import os
import json
import yaml
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path
import logging
from cryptography.fernet import Fernet
import base64

@dataclass
class ConfigSource:
    """Configuration source definition"""
    name: str
    path: str
    format: str  # json, yaml, env
    priority: int = 0
    encrypted: bool = False

@dataclass
class SystemConfig:
    """System configuration structure"""
    # Core system settings
    system_name: str = "AI Operating System Framework"
    version: str = "2.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Database configuration
    database_url: str = "sqlite:///aios.db"
    redis_url: str = "redis://localhost:6379"
    
    # Service configuration
    api_port: int = 8000
    dashboard_port: int = 3000
    cli_enabled: bool = True
    
    # Security settings
    encryption_key: Optional[str] = None
    jwt_secret: Optional[str] = None
    cors_origins: List[str] = field(default_factory=lambda: ["*"])
    
    # Agent execution settings
    max_concurrent_agents: int = 10
    agent_timeout_seconds: int = 300
    retry_attempts: int = 3
    
    # Monitoring and logging
    log_level: str = "INFO"
    metrics_enabled: bool = True
    health_check_interval: int = 30
    
    # Feature flags
    vector_search_enabled: bool = True
    self_healing_enabled: bool = True
    voice_agents_enabled: bool = False
    multi_modal_enabled: bool = False

class ConfigurationManager:
    """Professional configuration management system"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_sources: List[ConfigSource] = []
        self.config: SystemConfig = SystemConfig()
        self._encryption_key: Optional[bytes] = None
        self.logger = logging.getLogger(__name__)
        
        # Initialize configuration sources
        self._initialize_config_sources()
        
    def _initialize_config_sources(self):
        """Initialize configuration sources in priority order"""
        # Environment variables (highest priority)
        self.config_sources.append(ConfigSource(
            name="environment",
            path="",
            format="env",
            priority=100
        ))
        
        # Environment-specific config files
        env = os.getenv("ENVIRONMENT", "development")
        env_config_path = self.config_dir / f"config.{env}.yaml"
        if env_config_path.exists():
            self.config_sources.append(ConfigSource(
                name=f"config_{env}",
                path=str(env_config_path),
                format="yaml",
                priority=80
            ))
        
        # Default config file
        default_config_path = self.config_dir / "config.yaml"
        if default_config_path.exists():
            self.config_sources.append(ConfigSource(
                name="default_config",
                path=str(default_config_path),
                format="yaml",
                priority=50
            ))
        
        # Legacy JSON config (lowest priority)
        json_config_path = Path("config.json")
        if json_config_path.exists():
            self.config_sources.append(ConfigSource(
                name="legacy_json",
                path=str(json_config_path),
                format="json",
                priority=10
            ))
        
        # Sort by priority (highest first)
        self.config_sources.sort(key=lambda x: x.priority, reverse=True)
    
    def load_configuration(self) -> SystemConfig:
        """Load configuration from all sources"""
        config_data = {}
        
        # Load from each source in reverse priority order (lowest to highest)
        for source in reversed(self.config_sources):
            try:
                source_data = self._load_from_source(source)
                if source_data:
                    config_data.update(source_data)
                    self.logger.info(f"Loaded configuration from {source.name}")
            except Exception as e:
                self.logger.error(f"Failed to load config from {source.name}: {e}")
        
        # Create SystemConfig object from merged data
        self.config = self._create_config_object(config_data)
        
        # Validate configuration
        self._validate_configuration()
        
        return self.config
    
    def _load_from_source(self, source: ConfigSource) -> Optional[Dict[str, Any]]:
        """Load configuration from a specific source"""
        if source.format == "env":
            return self._load_from_environment()
        elif source.format == "yaml":
            return self._load_yaml_file(source.path, source.encrypted)
        elif source.format == "json":
            return self._load_json_file(source.path, source.encrypted)
        else:
            raise ValueError(f"Unsupported config format: {source.format}")
    
    def _load_from_environment(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        env_config = {}
        
        # Map environment variables to config keys
        env_mappings = {
            "AIOS_ENVIRONMENT": "environment",
            "AIOS_DEBUG": "debug",
            "AIOS_DATABASE_URL": "database_url",
            "AIOS_REDIS_URL": "redis_url",
            "AIOS_API_PORT": "api_port",
            "AIOS_DASHBOARD_PORT": "dashboard_port",
            "AIOS_ENCRYPTION_KEY": "encryption_key",
            "AIOS_JWT_SECRET": "jwt_secret",
            "AIOS_LOG_LEVEL": "log_level",
            "AIOS_MAX_CONCURRENT_AGENTS": "max_concurrent_agents",
            "AIOS_AGENT_TIMEOUT": "agent_timeout_seconds",
            "AIOS_RETRY_ATTEMPTS": "retry_attempts",
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Type conversion
                if config_key in ["debug", "cli_enabled", "metrics_enabled", 
                                "vector_search_enabled", "self_healing_enabled",
                                "voice_agents_enabled", "multi_modal_enabled"]:
                    env_config[config_key] = value.lower() in ("true", "1", "yes")
                elif config_key in ["api_port", "dashboard_port", "max_concurrent_agents",
                                  "agent_timeout_seconds", "retry_attempts", "health_check_interval"]:
                    env_config[config_key] = int(value)
                else:
                    env_config[config_key] = value
        
        return env_config
    
    def _load_yaml_file(self, file_path: str, encrypted: bool = False) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        with open(file_path, 'r') as f:
            content = f.read()
            
        if encrypted:
            content = self._decrypt_content(content)
            
        return yaml.safe_load(content)
    
    def _load_json_file(self, file_path: str, encrypted: bool = False) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        with open(file_path, 'r') as f:
            content = f.read()
            
        if encrypted:
            content = self._decrypt_content(content)
            
        return json.loads(content)
    
    def _decrypt_content(self, encrypted_content: str) -> str:
        """Decrypt configuration content"""
        if not self._encryption_key:
            self._encryption_key = self._get_encryption_key()
        
        fernet = Fernet(self._encryption_key)
        encrypted_bytes = base64.b64decode(encrypted_content.encode())
        decrypted_bytes = fernet.decrypt(encrypted_bytes)
        return decrypted_bytes.decode()
    
    def _get_encryption_key(self) -> bytes:
        """Get encryption key from environment or generate new one"""
        key_env = os.getenv("AIOS_MASTER_KEY")
        if key_env:
            return key_env.encode()
        
        # Generate new key (in production, this should be stored securely)
        key = Fernet.generate_key()
        self.logger.warning("Generated new encryption key. Store AIOS_MASTER_KEY securely!")
        return key
    
    def _create_config_object(self, config_data: Dict[str, Any]) -> SystemConfig:
        """Create SystemConfig object from dictionary"""
        # Filter only valid SystemConfig fields
        valid_fields = {field.name for field in SystemConfig.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in config_data.items() if k in valid_fields}
        
        return SystemConfig(**filtered_data)
    
    def _validate_configuration(self):
        """Validate the loaded configuration"""
        # Basic validation rules
        if self.config.max_concurrent_agents <= 0:
            raise ValueError("max_concurrent_agents must be positive")
        
        if self.config.agent_timeout_seconds <= 0:
            raise ValueError("agent_timeout_seconds must be positive")
        
        if self.config.api_port < 1 or self.config.api_port > 65535:
            raise ValueError("api_port must be between 1 and 65535")
        
        if self.config.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("log_level must be valid logging level")
        
        # Security validation
        if self.config.environment == "production":
            if not self.config.encryption_key:
                self.logger.warning("No encryption key set in production environment")
            if not self.config.jwt_secret:
                self.logger.warning("No JWT secret set in production environment")
            if self.config.debug:
                self.logger.warning("Debug mode enabled in production environment")
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get configuration specific to an agent"""
        # Load agent-specific configuration
        agent_config_path = self.config_dir / "agents" / f"{agent_name}.yaml"
        if agent_config_path.exists():
            return self._load_yaml_file(str(agent_config_path))
        return {}
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration at runtime"""
        try:
            # Update the current config
            for key, value in updates.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            
            # Validate after update
            self._validate_configuration()
            
            self.logger.info(f"Configuration updated: {list(updates.keys())}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {e}")
            return False
    
    def save_config(self, file_path: str = None, encrypt: bool = False):
        """Save current configuration to file"""
        if not file_path:
            file_path = self.config_dir / "config.current.yaml"
        
        # Convert config to dictionary
        config_dict = {
            field.name: getattr(self.config, field.name)
            for field in SystemConfig.__dataclass_fields__.values()
        }
        
        # Convert to YAML
        yaml_content = yaml.dump(config_dict, default_flow_style=False)
        
        if encrypt:
            yaml_content = self._encrypt_content(yaml_content)
        
        with open(file_path, 'w') as f:
            f.write(yaml_content)
        
        self.logger.info(f"Configuration saved to {file_path}")
    
    def _encrypt_content(self, content: str) -> str:
        """Encrypt configuration content"""
        if not self._encryption_key:
            self._encryption_key = self._get_encryption_key()
        
        fernet = Fernet(self._encryption_key)
        encrypted_bytes = fernet.encrypt(content.encode())
        return base64.b64encode(encrypted_bytes).decode()

# Global configuration manager instance
config_manager = ConfigurationManager()
