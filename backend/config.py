"""
Configuration management for AI Operating System Backend
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, Field, validator
from pathlib import Path

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Basic App Settings
    app_name: str = "AI Operating System API"
    app_version: str = "2.0.0"
    debug: bool = False
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server Settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    workers: int = Field(default=1, env="WORKERS")
    
    # Database Settings
    database_url: str = Field(default="sqlite:///./aimos.db", env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis Settings
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    # Security Settings
    secret_key: str = Field(default="aimos-super-secret-key-change-in-production", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS Settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        env="CORS_ORIGINS"
    )
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # Rate Limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Agent Execution Settings
    max_concurrent_agents: int = Field(default=5, env="MAX_CONCURRENT_AGENTS")
    agent_timeout_seconds: int = Field(default=300, env="AGENT_TIMEOUT_SECONDS")
    execution_retry_attempts: int = Field(default=3, env="EXECUTION_RETRY_ATTEMPTS")
    
    # Monitoring & Metrics
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_path: str = Field(default="/metrics", env="METRICS_PATH")
    health_check_path: str = Field(default="/health", env="HEALTH_CHECK_PATH")
    
    # Logging Settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json or text
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    
    # File Storage Settings
    upload_dir: str = Field(default="./uploads", env="UPLOAD_DIR")
    max_upload_size: int = Field(default=10 * 1024 * 1024, env="MAX_UPLOAD_SIZE")  # 10MB
    allowed_file_types: List[str] = Field(
        default=["pdf", "txt", "json", "csv", "xlsx"],
        env="ALLOWED_FILE_TYPES"
    )
    
    # AI/ML Settings
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    huggingface_api_key: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    
    # Vector Database Settings
    vector_db_type: str = Field(default="chroma", env="VECTOR_DB_TYPE")  # chroma, faiss, pinecone
    vector_db_url: Optional[str] = Field(default=None, env="VECTOR_DB_URL")
    vector_dimension: int = Field(default=1536, env="VECTOR_DIMENSION")
    
    # Background Task Settings
    celery_broker_url: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND")
    
    # WebSocket Settings
    websocket_ping_interval: int = Field(default=20, env="WEBSOCKET_PING_INTERVAL")
    websocket_ping_timeout: int = Field(default=10, env="WEBSOCKET_PING_TIMEOUT")
    max_websocket_connections: int = Field(default=100, env="MAX_WEBSOCKET_CONNECTIONS")
    
    # Cache Settings
    cache_ttl_seconds: int = Field(default=300, env="CACHE_TTL_SECONDS")
    cache_max_size: int = Field(default=1000, env="CACHE_MAX_SIZE")
    
    # Email Settings (for notifications)
    smtp_server: Optional[str] = Field(default=None, env="SMTP_SERVER")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    smtp_use_tls: bool = Field(default=True, env="SMTP_USE_TLS")
    
    # Webhook Settings
    webhook_secret: Optional[str] = Field(default=None, env="WEBHOOK_SECRET")
    webhook_timeout: int = Field(default=30, env="WEBHOOK_TIMEOUT")
    
    # Feature Flags
    enable_agent_auto_scaling: bool = Field(default=False, env="ENABLE_AGENT_AUTO_SCALING")
    enable_predictive_scaling: bool = Field(default=False, env="ENABLE_PREDICTIVE_SCALING")
    enable_self_healing: bool = Field(default=True, env="ENABLE_SELF_HEALING")
    enable_voice_agents: bool = Field(default=False, env="ENABLE_VOICE_AGENTS")
    enable_multi_modal: bool = Field(default=True, env="ENABLE_MULTI_MODAL")
    enable_distributed_execution: bool = Field(default=False, env="ENABLE_DISTRIBUTED_EXECUTION")
    
    # Advanced Security
    enable_2fa: bool = Field(default=False, env="ENABLE_2FA")
    session_timeout_minutes: int = Field(default=60, env="SESSION_TIMEOUT_MINUTES")
    max_login_attempts: int = Field(default=5, env="MAX_LOGIN_ATTEMPTS")
    lockout_duration_minutes: int = Field(default=15, env="LOCKOUT_DURATION_MINUTES")
    
    # Data Retention
    log_retention_days: int = Field(default=30, env="LOG_RETENTION_DAYS")
    metrics_retention_days: int = Field(default=90, env="METRICS_RETENTION_DAYS")
    execution_log_retention_days: int = Field(default=180, env="EXECUTION_LOG_RETENTION_DAYS")
    
    # Performance Settings
    connection_pool_size: int = Field(default=20, env="CONNECTION_POOL_SIZE")
    connection_pool_overflow: int = Field(default=10, env="CONNECTION_POOL_OVERFLOW")
    query_timeout_seconds: int = Field(default=30, env="QUERY_TIMEOUT_SECONDS")
    
    # Backup Settings
    auto_backup_enabled: bool = Field(default=True, env="AUTO_BACKUP_ENABLED")
    backup_interval_hours: int = Field(default=24, env="BACKUP_INTERVAL_HOURS")
    backup_retention_days: int = Field(default=30, env="BACKUP_RETENTION_DAYS")
    backup_location: str = Field(default="./backups", env="BACKUP_LOCATION")
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("allowed_file_types", pre=True)
    def parse_allowed_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(",")]
        return v
    
    @validator("environment")
    def validate_environment(cls, v):
        valid_environments = ["development", "staging", "production", "testing"]
        if v not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()
    
    @validator("vector_db_type")
    def validate_vector_db_type(cls, v):
        valid_types = ["chroma", "faiss", "pinecone", "weaviate", "qdrant"]
        if v not in valid_types:
            raise ValueError(f"Vector DB type must be one of: {valid_types}")
        return v
    
    def get_database_url(self) -> str:
        """Get database URL with proper formatting"""
        if self.database_url.startswith("postgresql://"):
            # Fix for SQLAlchemy 1.4+ which requires postgresql+psycopg2://
            return self.database_url.replace("postgresql://", "postgresql+psycopg2://")
        return self.database_url
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.upload_dir,
            self.backup_location,
            "./logs",
            "./data",
            "./cache"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    database_echo: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000"]

class ProductionSettings(Settings):
    """Production environment settings"""
    debug: bool = False
    log_level: str = "INFO"
    database_echo: bool = False
    enable_metrics: bool = True
    cors_origins: List[str] = []  # Should be set via environment variables

class TestingSettings(Settings):
    """Testing environment settings"""
    debug: bool = True
    log_level: str = "DEBUG"
    database_url: str = "sqlite:///./test.db"
    redis_url: str = "redis://localhost:6379/15"  # Use different DB for tests
    access_token_expire_minutes: int = 5  # Short expiry for tests

def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()

# Create directories on import
settings.create_directories()
