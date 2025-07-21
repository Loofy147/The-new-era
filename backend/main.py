"""
Advanced AI Operating System Backend API
High-performance FastAPI backend with authentication, real-time monitoring, and agent management
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from contextlib import asynccontextmanager
import sys
import os

# Add core orchestrator to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core', 'orchestrator'))

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, validator
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from redis import Redis
import jwt
from passlib.context import CryptContext
import httpx
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import structlog

# Import orchestrator components
from ai_orchestrator_architect import create_orchestrator
from workflow_designer import create_workflow_designer
from resource_manager import create_resource_manager
from decision_engine import create_decision_engine
from architecture_optimizer import create_architecture_optimizer
from performance_analyzer import create_performance_analyzer
from intelligence_coordinator import create_intelligence_coordinator

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger()

# Database configuration
DATABASE_URL = "sqlite:///./aimos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis for caching and real-time features
redis_client = Redis(host='localhost', port=6379, decode_responses=True, db=0)

# Security configuration
SECRET_KEY = "aimos-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Prometheus metrics
request_count = Counter('aimos_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('aimos_request_duration_seconds', 'HTTP request duration')
active_agents = Gauge('aimos_active_agents', 'Number of active agents')
system_health = Gauge('aimos_system_health_score', 'Overall system health score')

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    role = Column(String)
    description = Column(Text)
    status = Column(String, default="inactive")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_execution = Column(DateTime)
    success_rate = Column(Float, default=0.0)
    total_executions = Column(Integer, default=0)
    successful_executions = Column(Integer, default=0)

class ExecutionLog(Base):
    __tablename__ = "execution_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, index=True)
    agent_name = Column(String)
    status = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_ms = Column(Integer)
    result_data = Column(Text)
    error_message = Column(Text)
    metadata = Column(Text)

class SystemMetrics(Base):
    __tablename__ = "system_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    network_io = Column(Float)
    active_agents_count = Column(Integer)
    system_health_score = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=1000)

class AgentResponse(BaseModel):
    id: str
    name: str
    role: str
    description: str
    status: str
    created_at: datetime
    last_execution: Optional[datetime]
    success_rate: float
    total_executions: int
    successful_executions: int

class AgentUpdate(BaseModel):
    role: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ExecutionRequest(BaseModel):
    agent_ids: Optional[List[str]] = None
    parallel: bool = True
    timeout_seconds: int = 300

class ExecutionResponse(BaseModel):
    execution_id: str
    status: str
    started_at: datetime
    agent_count: int
    estimated_duration: int

class SystemStatus(BaseModel):
    status: str
    uptime_seconds: int
    version: str
    environment: str
    total_agents: int
    active_agents: int
    system_health_score: float
    last_execution: Optional[datetime]
    
class MetricsResponse(BaseModel):
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: float
    active_agents_count: int
    system_health_score: float

# Orchestrator Models
class OrchestratorTaskRequest(BaseModel):
    objective: str = Field(..., min_length=1, max_length=1000)
    required_capabilities: List[str] = Field(default=[])
    strategy: str = Field(default="hybrid")
    priority: int = Field(default=3, ge=1, le=5)
    timeout: int = Field(default=300, ge=30, le=3600)
    context: Dict[str, Any] = Field(default={})

class WorkflowRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)
    requirements: Dict[str, Any] = Field(default={})
    constraints: Dict[str, Any] = Field(default={})

class ResourceAllocationRequest(BaseModel):
    requester_id: str = Field(..., min_length=1)
    requirements: Dict[str, Any] = Field(...)
    strategy: str = Field(default="priority_based")

class PerformanceAnalysisRequest(BaseModel):
    analysis_type: str = Field(default="real_time")
    time_range_hours: int = Field(default=1, ge=1, le=168)
    metrics: List[str] = Field(default=[])

class IntelligenceCoordinationRequest(BaseModel):
    task: Dict[str, Any] = Field(...)
    agents: List[str] = Field(default=[])

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket

    def disconnect(self, websocket: WebSocket, user_id: str = None):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_json(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# Dependency functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Administrative privileges required")
    return current_user

# Background Tasks
async def collect_system_metrics():
    """Collect system metrics in background"""
    while True:
        try:
            # Simulate metrics collection
            import psutil
            
            cpu_usage = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Calculate system health score
            health_score = (
                (100 - cpu_usage) * 0.3 +
                (100 - memory.percent) * 0.3 +
                (100 - disk.percent) * 0.2 +
                90 * 0.2  # Base score for other factors
            ) / 100
            
            # Update Prometheus metrics
            system_health.set(health_score)
            
            # Store in database
            db = SessionLocal()
            try:
                metrics = SystemMetrics(
                    cpu_usage=cpu_usage,
                    memory_usage=memory.percent,
                    disk_usage=disk.percent,
                    network_io=0.0,  # Placeholder
                    active_agents_count=db.query(Agent).filter(Agent.status == "active").count(),
                    system_health_score=health_score
                )
                db.add(metrics)
                db.commit()
                
                # Broadcast to WebSocket clients
                await manager.broadcast({
                    "type": "metrics_update",
                    "data": {
                        "cpu_usage": cpu_usage,
                        "memory_usage": memory.percent,
                        "disk_usage": disk.percent,
                        "system_health_score": health_score,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                })
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error("Error collecting metrics", error=str(e))
        
        await asyncio.sleep(30)  # Collect every 30 seconds

# Initialize Orchestrator Components
orchestrator = None
workflow_designer = None
resource_manager = None
decision_engine = None
architecture_optimizer = None
performance_analyzer = None
intelligence_coordinator = None

# Startup/Shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator, workflow_designer, resource_manager, decision_engine
    global architecture_optimizer, performance_analyzer, intelligence_coordinator

    # Startup
    logger.info("Starting AI Operating System Backend API")

    # Initialize orchestrator components
    try:
        orchestrator = create_orchestrator()
        workflow_designer = create_workflow_designer()
        resource_manager = create_resource_manager()
        decision_engine = create_decision_engine()
        architecture_optimizer = create_architecture_optimizer()
        performance_analyzer = create_performance_analyzer()
        intelligence_coordinator = create_intelligence_coordinator()

        # Start orchestrator services
        await orchestrator.start()
        await resource_manager.start()
        await performance_analyzer.start_analysis()

        logger.info("AI Orchestrator system initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize orchestrator system", error=str(e))

    # Start background tasks
    asyncio.create_task(collect_system_metrics())

    # Initialize default admin user if not exists
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@aimos.local",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("Created default admin user")
    finally:
        db.close()

    yield

    # Shutdown
    logger.info("Shutting down AI Operating System Backend API")

    # Stop orchestrator services
    try:
        if orchestrator:
            await orchestrator.stop()
        if resource_manager:
            await resource_manager.stop()
        if performance_analyzer:
            await performance_analyzer.stop_analysis()
        logger.info("AI Orchestrator system stopped")
    except Exception as e:
        logger.error("Error stopping orchestrator system", error=str(e))

# FastAPI app
app = FastAPI(
    title="AI Operating System API",
    description="High-performance backend for AI agent management and monitoring",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middleware for metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = datetime.utcnow()
    
    # Track request
    request_count.labels(method=request.method, endpoint=request.url.path).inc()
    
    response = await call_next(request)
    
    # Track duration
    duration = (datetime.utcnow() - start_time).total_seconds()
    request_duration.observe(duration)
    
    return response

# Authentication Endpoints
@app.post("/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info("User registered", user_id=user.id, username=user.username)
    return user

@app.post("/api/auth/login", response_model=Token)
async def login(username: str, password: str, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    
    logger.info("User logged in", user_id=user.id, username=user.username)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

# Agent Management Endpoints
@app.get("/api/agents", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all agents with optional filtering"""
    
    query = db.query(Agent)
    if status:
        query = query.filter(Agent.status == status)
    
    agents = query.offset(skip).limit(limit).all()
    
    # Update active agents metric
    active_count = db.query(Agent).filter(Agent.status == "active").count()
    active_agents.set(active_count)
    
    return agents

@app.post("/api/agents", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Create a new agent (admin only)"""
    
    # Check if agent name exists
    if db.query(Agent).filter(Agent.name == agent_data.name).first():
        raise HTTPException(status_code=400, detail="Agent name already exists")
    
    agent = Agent(
        name=agent_data.name,
        role=agent_data.role,
        description=agent_data.description
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    logger.info("Agent created", agent_id=agent.id, agent_name=agent.name)
    
    # Broadcast to WebSocket clients
    await manager.broadcast({
        "type": "agent_created",
        "data": {
            "id": agent.id,
            "name": agent.name,
            "role": agent.role,
            "status": agent.status
        }
    })
    
    return agent

@app.get("/api/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get agent by ID"""
    
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent

@app.put("/api/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Update agent (admin only)"""
    
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    
    logger.info("Agent updated", agent_id=agent.id, agent_name=agent.name)
    
    # Broadcast to WebSocket clients
    await manager.broadcast({
        "type": "agent_updated",
        "data": {
            "id": agent.id,
            "name": agent.name,
            "role": agent.role,
            "status": agent.status
        }
    })
    
    return agent

@app.delete("/api/agents/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Delete agent (admin only)"""
    
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(agent)
    db.commit()
    
    logger.info("Agent deleted", agent_id=agent_id, agent_name=agent.name)
    
    # Broadcast to WebSocket clients
    await manager.broadcast({
        "type": "agent_deleted",
        "data": {"id": agent_id, "name": agent.name}
    })

# Execution Endpoints
@app.post("/api/execute", response_model=ExecutionResponse)
async def execute_agents(
    execution_request: ExecutionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute agents asynchronously"""
    
    execution_id = str(uuid.uuid4())
    
    # Get agents to execute
    if execution_request.agent_ids:
        agents = db.query(Agent).filter(Agent.id.in_(execution_request.agent_ids)).all()
    else:
        agents = db.query(Agent).filter(Agent.status == "active").all()
    
    if not agents:
        raise HTTPException(status_code=400, detail="No agents available for execution")
    
    # Add background task
    background_tasks.add_task(
        execute_agents_background,
        execution_id,
        [agent.id for agent in agents],
        execution_request.parallel,
        execution_request.timeout_seconds
    )
    
    logger.info("Execution started", 
                execution_id=execution_id, 
                agent_count=len(agents),
                parallel=execution_request.parallel)
    
    return ExecutionResponse(
        execution_id=execution_id,
        status="started",
        started_at=datetime.utcnow(),
        agent_count=len(agents),
        estimated_duration=len(agents) * 30 if not execution_request.parallel else 60
    )

async def execute_agents_background(execution_id: str, agent_ids: List[str], parallel: bool, timeout: int):
    """Background task for agent execution"""
    
    db = SessionLocal()
    try:
        # Broadcast execution start
        await manager.broadcast({
            "type": "execution_started",
            "data": {
                "execution_id": execution_id,
                "agent_count": len(agent_ids),
                "parallel": parallel
            }
        })
        
        results = []
        
        if parallel:
            # Execute agents in parallel
            tasks = [execute_single_agent(agent_id, execution_id) for agent_id in agent_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            # Execute agents sequentially
            for agent_id in agent_ids:
                result = await execute_single_agent(agent_id, execution_id)
                results.append(result)
        
        # Process results
        successful = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "success")
        failed = len(results) - successful
        
        # Update agent statistics
        for i, agent_id in enumerate(agent_ids):
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if agent:
                agent.total_executions += 1
                agent.last_execution = datetime.utcnow()
                
                if isinstance(results[i], dict) and results[i].get("status") == "success":
                    agent.successful_executions += 1
                
                agent.success_rate = (agent.successful_executions / agent.total_executions) * 100
                
        db.commit()
        
        # Broadcast execution completion
        await manager.broadcast({
            "type": "execution_completed",
            "data": {
                "execution_id": execution_id,
                "total_agents": len(agent_ids),
                "successful": successful,
                "failed": failed,
                "success_rate": (successful / len(agent_ids)) * 100
            }
        })
        
        logger.info("Execution completed",
                    execution_id=execution_id,
                    successful=successful,
                    failed=failed)
        
    except Exception as e:
        logger.error("Execution failed", execution_id=execution_id, error=str(e))
        await manager.broadcast({
            "type": "execution_failed",
            "data": {
                "execution_id": execution_id,
                "error": str(e)
            }
        })
    finally:
        db.close()

async def execute_single_agent(agent_id: str, execution_id: str) -> Dict[str, Any]:
    """Execute a single agent"""
    
    start_time = datetime.utcnow()
    db = SessionLocal()
    
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if not agent:
            raise Exception(f"Agent {agent_id} not found")
        
        # Simulate agent execution
        await asyncio.sleep(2)  # Simulate work
        
        # 90% success rate simulation
        import random
        success = random.random() < 0.9
        
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Log execution
        log_entry = ExecutionLog(
            agent_id=agent_id,
            agent_name=agent.name,
            status="success" if success else "failed",
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration_ms,
            result_data=json.dumps({"message": "Agent executed successfully"}) if success else None,
            error_message=None if success else "Simulated failure",
            metadata=json.dumps({"execution_id": execution_id})
        )
        
        db.add(log_entry)
        db.commit()
        
        # Broadcast agent completion
        await manager.broadcast({
            "type": "agent_completed",
            "data": {
                "execution_id": execution_id,
                "agent_id": agent_id,
                "agent_name": agent.name,
                "status": "success" if success else "failed",
                "duration_ms": duration_ms
            }
        })
        
        return {
            "agent_id": agent_id,
            "agent_name": agent.name,
            "status": "success" if success else "failed",
            "duration_ms": duration_ms
        }
        
    except Exception as e:
        end_time = datetime.utcnow()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)
        
        # Log error
        log_entry = ExecutionLog(
            agent_id=agent_id,
            agent_name=agent.name if 'agent' in locals() else "Unknown",
            status="error",
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration_ms,
            error_message=str(e),
            metadata=json.dumps({"execution_id": execution_id})
        )
        
        db.add(log_entry)
        db.commit()
        
        return {
            "agent_id": agent_id,
            "status": "error",
            "error": str(e),
            "duration_ms": duration_ms
        }
    finally:
        db.close()

# System Endpoints
@app.get("/api/system/status", response_model=SystemStatus)
async def get_system_status(db: Session = Depends(get_db)):
    """Get system status and health"""
    
    total_agents = db.query(Agent).count()
    active_agents_count = db.query(Agent).filter(Agent.status == "active").count()
    
    # Get latest metrics
    latest_metrics = db.query(SystemMetrics).order_by(SystemMetrics.timestamp.desc()).first()
    health_score = latest_metrics.system_health_score if latest_metrics else 0.0
    
    # Get last execution
    last_execution = db.query(ExecutionLog).order_by(ExecutionLog.start_time.desc()).first()
    
    return SystemStatus(
        status="healthy" if health_score > 0.8 else "warning" if health_score > 0.6 else "critical",
        uptime_seconds=int((datetime.utcnow() - datetime(2024, 1, 1)).total_seconds()),
        version="2.0.0",
        environment="production",
        total_agents=total_agents,
        active_agents=active_agents_count,
        system_health_score=health_score,
        last_execution=last_execution.start_time if last_execution else None
    )

@app.get("/api/system/metrics", response_model=List[MetricsResponse])
async def get_system_metrics(
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get system metrics for the specified time period"""
    
    since = datetime.utcnow() - timedelta(hours=hours)
    metrics = db.query(SystemMetrics).filter(
        SystemMetrics.timestamp >= since
    ).order_by(SystemMetrics.timestamp.desc()).all()
    
    return metrics

@app.get("/api/system/metrics/prometheus")
async def get_prometheus_metrics():
    """Get Prometheus metrics"""
    return StreamingResponse(
        iter([generate_latest().decode('utf-8')]),
        media_type="text/plain"
    )

# Execution Logs
@app.get("/api/executions")
async def get_execution_logs(
    skip: int = 0,
    limit: int = 100,
    agent_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get execution logs with filtering"""
    
    query = db.query(ExecutionLog)
    
    if agent_id:
        query = query.filter(ExecutionLog.agent_id == agent_id)
    if status:
        query = query.filter(ExecutionLog.status == status)
    
    logs = query.order_by(ExecutionLog.start_time.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "agent_id": log.agent_id,
            "agent_name": log.agent_name,
            "status": log.status,
            "start_time": log.start_time,
            "end_time": log.end_time,
            "duration_ms": log.duration_ms,
            "error_message": log.error_message
        }
        for log in logs
    ]

# WebSocket Endpoint
@app.websocket("/api/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time updates"""
    
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for testing
            await websocket.send_json({"type": "echo", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# Orchestrator Endpoints
@app.post("/api/orchestrator/tasks")
async def create_orchestrated_task(
    task_request: OrchestratorTaskRequest,
    current_user: User = Depends(get_current_user)
):
    """Create and execute an orchestrated task"""

    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator service not available")

    try:
        task_id = await orchestrator.execute_task(
            objective=task_request.objective,
            required_capabilities=task_request.required_capabilities,
            strategy=task_request.strategy,
            priority=task_request.priority,
            timeout=task_request.timeout,
            context=task_request.context
        )

        logger.info("Orchestrated task created", task_id=task_id, user_id=current_user.id)

        return {
            "task_id": task_id,
            "status": "created",
            "objective": task_request.objective,
            "estimated_duration": task_request.timeout
        }
    except Exception as e:
        logger.error("Failed to create orchestrated task", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestrator/tasks/{task_id}")
async def get_orchestrated_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get orchestrated task status and results"""

    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator service not available")

    try:
        task_status = await orchestrator.get_task_status(task_id)
        if not task_status:
            raise HTTPException(status_code=404, detail="Task not found")

        return task_status
    except Exception as e:
        logger.error("Failed to get task status", task_id=task_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/orchestrator/workflows")
async def create_workflow(
    workflow_request: WorkflowRequest,
    current_user: User = Depends(get_admin_user)
):
    """Create a new workflow template"""

    if not workflow_designer:
        raise HTTPException(status_code=503, detail="Workflow designer service not available")

    try:
        workflow_template = await workflow_designer.design_adaptive_workflow(
            requirements=workflow_request.requirements,
            constraints=workflow_request.constraints
        )

        workflow_template.name = workflow_request.name
        workflow_template.description = workflow_request.description

        workflow_designer.template_library.add_template(workflow_template)

        logger.info("Workflow created", workflow_name=workflow_request.name, user_id=current_user.id)

        return {
            "workflow_name": workflow_request.name,
            "status": "created",
            "node_count": len(workflow_template.nodes),
            "description": workflow_request.description
        }
    except Exception as e:
        logger.error("Failed to create workflow", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestrator/workflows")
async def list_workflows(current_user: User = Depends(get_current_user)):
    """List available workflow templates"""

    if not workflow_designer:
        raise HTTPException(status_code=503, detail="Workflow designer service not available")

    try:
        templates = workflow_designer.template_library.list_templates()
        return {"workflows": templates}
    except Exception as e:
        logger.error("Failed to list workflows", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/orchestrator/resources/allocate")
async def allocate_resources(
    allocation_request: ResourceAllocationRequest,
    current_user: User = Depends(get_current_user)
):
    """Allocate system resources"""

    if not resource_manager:
        raise HTTPException(status_code=503, detail="Resource manager service not available")

    try:
        allocation_ids = await resource_manager.allocate_resources(
            allocation_request.requester_id,
            allocation_request.requirements
        )

        logger.info("Resources allocated",
                   requester_id=allocation_request.requester_id,
                   allocations=allocation_ids)

        return {
            "allocation_ids": allocation_ids,
            "status": "allocated",
            "requester_id": allocation_request.requester_id
        }
    except Exception as e:
        logger.error("Failed to allocate resources", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestrator/resources/status")
async def get_resource_status(current_user: User = Depends(get_current_user)):
    """Get system resource status"""

    if not resource_manager:
        raise HTTPException(status_code=503, detail="Resource manager service not available")

    try:
        status = resource_manager.get_system_status()
        return status
    except Exception as e:
        logger.error("Failed to get resource status", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/orchestrator/performance/analyze")
async def analyze_performance(
    analysis_request: PerformanceAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """Perform performance analysis"""

    if not performance_analyzer:
        raise HTTPException(status_code=503, detail="Performance analyzer service not available")

    try:
        from performance_analyzer import AnalysisType
        analysis_type = AnalysisType(analysis_request.analysis_type)

        report = await performance_analyzer.perform_analysis(analysis_type)

        logger.info("Performance analysis completed",
                   analysis_id=report.analysis_id,
                   performance_score=report.performance_score)

        return {
            "analysis_id": report.analysis_id,
            "analysis_type": report.analysis_type.value,
            "performance_score": report.performance_score,
            "bottlenecks": report.bottlenecks,
            "recommendations": report.recommendations,
            "alert_count": len(report.alerts)
        }
    except Exception as e:
        logger.error("Failed to analyze performance", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestrator/performance/insights")
async def get_performance_insights(current_user: User = Depends(get_current_user)):
    """Get performance insights and trends"""

    if not performance_analyzer:
        raise HTTPException(status_code=503, detail="Performance analyzer service not available")

    try:
        insights = await performance_analyzer.get_performance_insights()
        return insights
    except Exception as e:
        logger.error("Failed to get performance insights", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/orchestrator/intelligence/coordinate")
async def coordinate_intelligence(
    coordination_request: IntelligenceCoordinationRequest,
    current_user: User = Depends(get_current_user)
):
    """Coordinate intelligence across agents"""

    if not intelligence_coordinator:
        raise HTTPException(status_code=503, detail="Intelligence coordinator service not available")

    try:
        result = await intelligence_coordinator.coordinate_intelligence(coordination_request.task)

        logger.info("Intelligence coordination completed",
                   coordination_id=result["coordination_id"],
                   status=result["status"])

        return result
    except Exception as e:
        logger.error("Failed to coordinate intelligence", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestrator/intelligence/patterns")
async def get_coordination_patterns(current_user: User = Depends(get_current_user)):
    """Get intelligence coordination patterns and insights"""

    if not intelligence_coordinator:
        raise HTTPException(status_code=503, detail="Intelligence coordinator service not available")

    try:
        patterns = await intelligence_coordinator.analyze_coordination_patterns()
        return patterns
    except Exception as e:
        logger.error("Failed to get coordination patterns", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestrator/architecture/optimize")
async def optimize_architecture(current_user: User = Depends(get_admin_user)):
    """Optimize system architecture"""

    if not architecture_optimizer:
        raise HTTPException(status_code=503, detail="Architecture optimizer service not available")

    try:
        from architecture_optimizer import OptimizationObjective
        objectives = [
            OptimizationObjective.PERFORMANCE,
            OptimizationObjective.SCALABILITY,
            OptimizationObjective.RELIABILITY
        ]

        optimization_report = await architecture_optimizer.optimize_architecture(objectives)

        logger.info("Architecture optimization completed",
                   overall_score=optimization_report["current_metrics"]["overall_score"])

        return optimization_report
    except Exception as e:
        logger.error("Failed to optimize architecture", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orchestrator/status")
async def get_orchestrator_status(current_user: User = Depends(get_current_user)):
    """Get overall orchestrator system status"""

    try:
        status = {
            "orchestrator": orchestrator is not None,
            "workflow_designer": workflow_designer is not None,
            "resource_manager": resource_manager is not None,
            "decision_engine": decision_engine is not None,
            "architecture_optimizer": architecture_optimizer is not None,
            "performance_analyzer": performance_analyzer is not None,
            "intelligence_coordinator": intelligence_coordinator is not None,
            "timestamp": datetime.utcnow()
        }

        # Get additional status information if services are available
        if resource_manager:
            status["resource_status"] = resource_manager.get_system_status()

        if performance_analyzer:
            status["performance_insights"] = await performance_analyzer.get_performance_insights()

        return status
    except Exception as e:
        logger.error("Failed to get orchestrator status", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Health Check
@app.get("/api/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
