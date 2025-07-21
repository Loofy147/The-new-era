# AI Operating System - API Integration Guide

## Overview

This comprehensive guide covers all available APIs for integrating with the AI Operating System. The system provides RESTful APIs, WebSocket connections, and real-time data streaming for seamless integration with external services and applications.

## Base Configuration

### Environment Variables
```bash
# Backend API
REACT_APP_API_URL=http://localhost:8000/api
API_BASE_URL=http://localhost:8000

# Authentication
NEXT_PUBLIC_STACK_PROJECT_ID=your_stack_project_id
NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY=your_publishable_key
STACK_SECRET_SERVER_KEY=your_secret_key

# Database
DATABASE_URL=postgresql://username:password@host:port/database
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### API Authentication

All API endpoints (except health check and auth) require JWT authentication:

```javascript
// Include in headers
Authorization: Bearer {access_token}
Content-Type: application/json
```

## Core API Endpoints

### 1. Authentication APIs

#### POST /api/auth/register
Register a new user account.

```javascript
// Request
{
  "username": "john_doe",
  "email": "john@example.com", 
  "password": "secure_password123"
}

// Response (201 Created)
{
  "id": "uuid",
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": null
}
```

#### POST /api/auth/login
Authenticate user and get access token.

```javascript
// Request (Form Data)
username=john_doe&password=secure_password123

// Response (200 OK)
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### GET /api/auth/me
Get current user profile.

```javascript
// Response (200 OK)
{
  "id": "uuid",
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-15T11:00:00Z"
}
```

### 2. Agent Management APIs

#### GET /api/agents
List all agents with optional filtering.

```javascript
// Query Parameters
skip=0&limit=100&status=active

// Response (200 OK)
[
  {
    "id": "agent_uuid",
    "name": "CostOptBot",
    "role": "Cost Optimization & Analysis",
    "description": "Analyzes infrastructure costs and identifies savings",
    "status": "active",
    "created_at": "2024-01-15T09:00:00Z",
    "last_execution": "2024-01-15T11:30:00Z",
    "success_rate": 94.5,
    "total_executions": 127,
    "successful_executions": 120
  }
]
```

#### POST /api/agents
Create a new agent (Admin only).

```javascript
// Request
{
  "name": "CustomBot",
  "role": "Custom Analysis",
  "description": "Performs custom business analysis tasks"
}

// Response (201 Created)
{
  "id": "new_agent_uuid",
  "name": "CustomBot",
  "role": "Custom Analysis", 
  "description": "Performs custom business analysis tasks",
  "status": "inactive",
  "created_at": "2024-01-15T12:00:00Z",
  "last_execution": null,
  "success_rate": 0.0,
  "total_executions": 0,
  "successful_executions": 0
}
```

#### GET /api/agents/{agent_id}
Get specific agent details.

#### PUT /api/agents/{agent_id}
Update agent configuration (Admin only).

```javascript
// Request
{
  "role": "Enhanced Custom Analysis",
  "description": "Updated description with new capabilities",
  "status": "active"
}
```

#### DELETE /api/agents/{agent_id}
Delete agent (Admin only).

### 3. Execution APIs

#### POST /api/execute
Execute agents asynchronously.

```javascript
// Request
{
  "agent_ids": ["agent1_uuid", "agent2_uuid"], // Optional, all active if omitted
  "parallel": true,
  "timeout_seconds": 300
}

// Response (200 OK)
{
  "execution_id": "execution_uuid",
  "status": "started",
  "started_at": "2024-01-15T12:00:00Z",
  "agent_count": 2,
  "estimated_duration": 60
}
```

#### GET /api/executions
Get execution logs with filtering.

```javascript
// Query Parameters
skip=0&limit=50&agent_id=uuid&status=success

// Response (200 OK)
[
  {
    "id": "log_uuid",
    "agent_id": "agent_uuid",
    "agent_name": "CostOptBot",
    "status": "success",
    "start_time": "2024-01-15T11:30:00Z",
    "end_time": "2024-01-15T11:32:30Z",
    "duration_ms": 150000,
    "error_message": null
  }
]
```

### 4. System APIs

#### GET /api/system/status
Get comprehensive system status.

```javascript
// Response (200 OK)
{
  "status": "healthy",
  "uptime_seconds": 86400,
  "version": "2.0.0",
  "environment": "production",
  "total_agents": 9,
  "active_agents": 8,
  "system_health_score": 0.94,
  "last_execution": "2024-01-15T11:30:00Z"
}
```

#### GET /api/system/metrics
Get system metrics for specified time period.

```javascript
// Query Parameters
hours=24

// Response (200 OK)
[
  {
    "timestamp": "2024-01-15T11:00:00Z",
    "cpu_usage": 34.5,
    "memory_usage": 67.2,
    "disk_usage": 45.8,
    "network_io": 23.1,
    "active_agents_count": 8,
    "system_health_score": 0.94
  }
]
```

#### GET /api/system/metrics/prometheus
Get Prometheus-formatted metrics.

```text
# HELP aimos_requests_total Total HTTP requests
# TYPE aimos_requests_total counter
aimos_requests_total{method="GET",endpoint="/api/agents"} 150
aimos_requests_total{method="POST",endpoint="/api/execute"} 45

# HELP aimos_active_agents Number of active agents
# TYPE aimos_active_agents gauge
aimos_active_agents 8

# HELP aimos_system_health_score Overall system health score
# TYPE aimos_system_health_score gauge
aimos_system_health_score 0.94
```

### 5. WebSocket APIs

#### WS /api/ws/{user_id}
Real-time updates and notifications.

```javascript
// Connection
const ws = new WebSocket('ws://localhost:8000/api/ws/user123');

// Message Types Received
{
  "type": "metrics_update",
  "data": {
    "cpu_usage": 35.2,
    "memory_usage": 68.1,
    "system_health_score": 0.93,
    "timestamp": "2024-01-15T12:00:00Z"
  }
}

{
  "type": "execution_started",
  "data": {
    "execution_id": "exec_uuid",
    "agent_count": 5,
    "parallel": true
  }
}

{
  "type": "agent_completed",
  "data": {
    "execution_id": "exec_uuid",
    "agent_id": "agent_uuid",
    "agent_name": "CostOptBot",
    "status": "success",
    "duration_ms": 2500
  }
}

{
  "type": "execution_completed",
  "data": {
    "execution_id": "exec_uuid",
    "total_agents": 5,
    "successful": 4,
    "failed": 1,
    "success_rate": 80.0
  }
}
```

## Advanced Integration Examples

### 1. JavaScript/React Integration

```javascript
import apiService from './services/api';

// Initialize API service
const api = apiService;

// Authentication flow
async function authenticateUser(username, password) {
  try {
    const response = await api.login(username, password);
    console.log('Login successful:', response);
    
    // Get user profile
    const user = await api.getCurrentUser();
    console.log('User profile:', user);
    
    return { success: true, user };
  } catch (error) {
    console.error('Authentication failed:', error);
    return { success: false, error: error.message };
  }
}

// Agent management
async function manageAgents() {
  try {
    // Get all active agents
    const agents = await api.getAgents({ status: 'active' });
    console.log('Active agents:', agents);
    
    // Execute specific agents
    const execution = await api.executeAgents({
      agent_ids: agents.slice(0, 3).map(a => a.id),
      parallel: true,
      timeout_seconds: 300
    });
    console.log('Execution started:', execution);
    
    return execution;
  } catch (error) {
    console.error('Agent management failed:', error);
  }
}

// Real-time monitoring
function setupRealTimeMonitoring(userId) {
  const ws = api.createWebSocketConnection(userId);
  
  ws.onopen = () => {
    console.log('WebSocket connected');
  };
  
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    
    switch (message.type) {
      case 'metrics_update':
        updateDashboardMetrics(message.data);
        break;
      case 'execution_completed':
        showExecutionResults(message.data);
        break;
      case 'agent_created':
        refreshAgentList();
        break;
    }
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  return ws;
}
```

### 2. Python Integration

```python
import requests
import json
from typing import Dict, List, Optional

class AIMOSClient:
    def __init__(self, base_url: str, username: str = None, password: str = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None
        
        if username and password:
            self.login(username, password)
    
    def login(self, username: str, password: str) -> Dict:
        """Authenticate and get access token"""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        
        data = response.json()
        self.token = data["access_token"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}"
        })
        
        return data
    
    def get_agents(self, status: Optional[str] = None) -> List[Dict]:
        """Get list of agents"""
        params = {}
        if status:
            params["status"] = status
            
        response = self.session.get(
            f"{self.base_url}/agents",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def execute_agents(self, agent_ids: List[str] = None, 
                      parallel: bool = True, 
                      timeout_seconds: int = 300) -> Dict:
        """Execute agents"""
        payload = {
            "parallel": parallel,
            "timeout_seconds": timeout_seconds
        }
        if agent_ids:
            payload["agent_ids"] = agent_ids
            
        response = self.session.post(
            f"{self.base_url}/execute",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_system_status(self) -> Dict:
        """Get system status"""
        response = self.session.get(f"{self.base_url}/system/status")
        response.raise_for_status()
        return response.json()
    
    def get_execution_logs(self, agent_id: str = None, 
                          status: str = None, 
                          limit: int = 100) -> List[Dict]:
        """Get execution logs"""
        params = {"limit": limit}
        if agent_id:
            params["agent_id"] = agent_id
        if status:
            params["status"] = status
            
        response = self.session.get(
            f"{self.base_url}/executions",
            params=params
        )
        response.raise_for_status()
        return response.json()

# Usage example
client = AIMOSClient("http://localhost:8000/api", "admin", "admin123")

# Get system status
status = client.get_system_status()
print(f"System Health: {status['system_health_score']}")

# Get active agents
agents = client.get_agents(status="active")
print(f"Active Agents: {len(agents)}")

# Execute all agents
execution = client.execute_agents(parallel=True)
print(f"Execution ID: {execution['execution_id']}")
```

### 3. Node.js Integration

```javascript
const axios = require('axios');
const WebSocket = require('ws');

class AIMOSClient {
  constructor(baseUrl, username = null, password = null) {
    this.baseUrl = baseUrl.replace(/\/$/, '');
    this.token = null;
    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Add request interceptor for authentication
    this.client.interceptors.request.use(config => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });
    
    if (username && password) {
      this.login(username, password);
    }
  }
  
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await this.client.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    
    this.token = response.data.access_token;
    return response.data;
  }
  
  async getAgents(filters = {}) {
    const response = await this.client.get('/agents', { params: filters });
    return response.data;
  }
  
  async executeAgents(options = {}) {
    const response = await this.client.post('/execute', options);
    return response.data;
  }
  
  async getSystemStatus() {
    const response = await this.client.get('/system/status');
    return response.data;
  }
  
  createWebSocketConnection(userId) {
    const wsUrl = `${this.baseUrl.replace('http', 'ws')}/ws/${userId}`;
    const ws = new WebSocket(wsUrl);
    
    ws.on('open', () => {
      console.log('WebSocket connected');
    });
    
    ws.on('message', (data) => {
      const message = JSON.parse(data);
      this.handleWebSocketMessage(message);
    });
    
    return ws;
  }
  
  handleWebSocketMessage(message) {
    console.log('WebSocket message:', message);
    // Override this method to handle specific message types
  }
}

// Usage
const client = new AIMOSClient('http://localhost:8000/api');

async function main() {
  try {
    await client.login('admin', 'admin123');
    
    const status = await client.getSystemStatus();
    console.log('System Status:', status);
    
    const agents = await client.getAgents({ status: 'active' });
    console.log('Active Agents:', agents.length);
    
    const execution = await client.executeAgents({
      parallel: true,
      timeout_seconds: 300
    });
    console.log('Execution Started:', execution.execution_id);
    
    // Setup WebSocket monitoring
    const ws = client.createWebSocketConnection('user123');
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

main();
```

## Error Handling

### Standard Error Responses

```javascript
// 400 Bad Request
{
  "detail": "Invalid request data",
  "type": "validation_error",
  "errors": [
    {
      "field": "username",
      "message": "Username must be at least 3 characters"
    }
  ]
}

// 401 Unauthorized
{
  "detail": "Invalid authentication credentials"
}

// 403 Forbidden
{
  "detail": "Administrative privileges required"
}

// 404 Not Found
{
  "detail": "Agent not found"
}

// 429 Too Many Requests
{
  "detail": "Rate limit exceeded",
  "retry_after": 60
}

// 500 Internal Server Error
{
  "detail": "Internal server error",
  "error_id": "uuid_for_tracking"
}
```

### Best Practices for Error Handling

1. **Always check response status codes**
2. **Implement retry logic for transient errors**
3. **Handle authentication expiration gracefully**
4. **Log errors with sufficient context**
5. **Provide user-friendly error messages**

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Default Limit**: 100 requests per minute per user
- **Admin Users**: 200 requests per minute
- **WebSocket Connections**: 100 concurrent connections per user

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1642248000
```

## Webhook Integration

Configure webhooks to receive real-time notifications:

```javascript
// Webhook payload example
{
  "event": "agent.execution.completed",
  "timestamp": "2024-01-15T12:00:00Z",
  "data": {
    "execution_id": "uuid",
    "agent_id": "uuid",
    "agent_name": "CostOptBot",
    "status": "success",
    "duration_ms": 2500,
    "result": {
      "savings_identified": 2340,
      "recommendations": 5
    }
  },
  "signature": "sha256=hash_for_verification"
}
```

## Security Considerations

1. **Use HTTPS in production**
2. **Implement proper CORS policies**
3. **Validate webhook signatures**
4. **Store API tokens securely**
5. **Implement proper session management**
6. **Use environment variables for sensitive data**
7. **Monitor for suspicious activity**

## Performance Optimization

1. **Use pagination for large datasets**
2. **Implement client-side caching**
3. **Batch API requests when possible**
4. **Use WebSockets for real-time data**
5. **Implement connection pooling**
6. **Monitor API response times**

## Support and Resources

- **API Documentation**: `/api/docs` (Swagger UI)
- **API Schema**: `/api/redoc` (ReDoc)
- **Health Check**: `/api/health`
- **Metrics**: `/api/system/metrics/prometheus`

For additional support, please refer to the main documentation or contact the development team.
