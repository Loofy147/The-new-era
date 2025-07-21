/**
 * AI Operating System API Service
 * Centralized API client for all backend interactions
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  getAuthHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getAuthHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      // Handle different response types
      const contentType = response.headers.get('content-type');
      let data;
      
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (!response.ok) {
        throw new ApiError(
          data.detail || data.message || `HTTP ${response.status}`,
          response.status,
          data
        );
      }

      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      
      // Network or other errors
      throw new ApiError(
        'Network error or server unavailable',
        0,
        { originalError: error.message }
      );
    }
  }

  // Authentication Methods
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await this.makeRequest('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    this.setToken(response.access_token);
    return response;
  }

  async register(userData) {
    return this.makeRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser() {
    return this.makeRequest('/auth/me');
  }

  logout() {
    this.setToken(null);
  }

  // Agent Management Methods
  async getAgents(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/agents?${query}` : '/agents';
    return this.makeRequest(endpoint);
  }

  async getAgent(agentId) {
    return this.makeRequest(`/agents/${agentId}`);
  }

  async createAgent(agentData) {
    return this.makeRequest('/agents', {
      method: 'POST',
      body: JSON.stringify(agentData),
    });
  }

  async updateAgent(agentId, agentData) {
    return this.makeRequest(`/agents/${agentId}`, {
      method: 'PUT',
      body: JSON.stringify(agentData),
    });
  }

  async deleteAgent(agentId) {
    return this.makeRequest(`/agents/${agentId}`, {
      method: 'DELETE',
    });
  }

  // Execution Methods
  async executeAgents(executionRequest) {
    return this.makeRequest('/execute', {
      method: 'POST',
      body: JSON.stringify(executionRequest),
    });
  }

  async getExecutionLogs(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/executions?${query}` : '/executions';
    return this.makeRequest(endpoint);
  }

  // System Methods
  async getSystemStatus() {
    return this.makeRequest('/system/status');
  }

  async getSystemMetrics(hours = 24) {
    return this.makeRequest(`/system/metrics?hours=${hours}`);
  }

  async getPrometheusMetrics() {
    return this.makeRequest('/system/metrics/prometheus', {
      headers: {
        ...this.getAuthHeaders(),
        'Accept': 'text/plain',
      },
    });
  }

  // Health Check
  async healthCheck() {
    return this.makeRequest('/health');
  }

  // WebSocket Connection
  createWebSocketConnection(userId) {
    const wsUrl = `${this.baseURL.replace('http', 'ws')}/ws/${userId}`;
    return new WebSocket(wsUrl);
  }

  // File Upload (if needed)
  async uploadFile(file, endpoint = '/upload') {
    const formData = new FormData();
    formData.append('file', file);

    return this.makeRequest(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        // Don't set Content-Type for FormData
      },
      body: formData,
    });
  }

  // Bulk Operations
  async bulkUpdateAgents(updates) {
    return this.makeRequest('/agents/bulk', {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async bulkDeleteAgents(agentIds) {
    return this.makeRequest('/agents/bulk', {
      method: 'DELETE',
      body: JSON.stringify({ agent_ids: agentIds }),
    });
  }

  // Analytics and Reporting
  async getExecutionAnalytics(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/analytics/executions?${query}` : '/analytics/executions';
    return this.makeRequest(endpoint);
  }

  async getAgentPerformance(agentId, timeRange = '7d') {
    return this.makeRequest(`/analytics/agents/${agentId}/performance?range=${timeRange}`);
  }

  async getSystemInsights(timeRange = '24h') {
    return this.makeRequest(`/analytics/system/insights?range=${timeRange}`);
  }

  // Configuration Management
  async getConfiguration() {
    return this.makeRequest('/config');
  }

  async updateConfiguration(configData) {
    return this.makeRequest('/config', {
      method: 'PUT',
      body: JSON.stringify(configData),
    });
  }

  // User Management (Admin only)
  async getUsers(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/admin/users?${query}` : '/admin/users';
    return this.makeRequest(endpoint);
  }

  async createUser(userData) {
    return this.makeRequest('/admin/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async updateUser(userId, userData) {
    return this.makeRequest(`/admin/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async deleteUser(userId) {
    return this.makeRequest(`/admin/users/${userId}`, {
      method: 'DELETE',
    });
  }

  // Notification Management
  async getNotifications(params = {}) {
    const query = new URLSearchParams(params).toString();
    const endpoint = query ? `/notifications?${query}` : '/notifications';
    return this.makeRequest(endpoint);
  }

  async markNotificationRead(notificationId) {
    return this.makeRequest(`/notifications/${notificationId}/read`, {
      method: 'PUT',
    });
  }

  async markAllNotificationsRead() {
    return this.makeRequest('/notifications/read-all', {
      method: 'PUT',
    });
  }

  // Search and Filtering
  async searchAgents(query, filters = {}) {
    return this.makeRequest('/search/agents', {
      method: 'POST',
      body: JSON.stringify({ query, filters }),
    });
  }

  async searchExecutions(query, filters = {}) {
    return this.makeRequest('/search/executions', {
      method: 'POST',
      body: JSON.stringify({ query, filters }),
    });
  }

  // Real-time Data Streaming
  async streamMetrics(callback) {
    const eventSource = new EventSource(`${this.baseURL}/stream/metrics`, {
      headers: this.getAuthHeaders(),
    });

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        callback(data);
      } catch (error) {
        console.error('Error parsing streaming data:', error);
      }
    };

    eventSource.onerror = (error) => {
      console.error('EventSource failed:', error);
      eventSource.close();
    };

    return eventSource;
  }

  // Integration Management
  async getIntegrations() {
    return this.makeRequest('/integrations');
  }

  async createIntegration(integrationData) {
    return this.makeRequest('/integrations', {
      method: 'POST',
      body: JSON.stringify(integrationData),
    });
  }

  async updateIntegration(integrationId, integrationData) {
    return this.makeRequest(`/integrations/${integrationId}`, {
      method: 'PUT',
      body: JSON.stringify(integrationData),
    });
  }

  async deleteIntegration(integrationId) {
    return this.makeRequest(`/integrations/${integrationId}`, {
      method: 'DELETE',
    });
  }

  async testIntegration(integrationId) {
    return this.makeRequest(`/integrations/${integrationId}/test`, {
      method: 'POST',
    });
  }

  // Backup and Export
  async exportData(dataType, format = 'json') {
    return this.makeRequest(`/export/${dataType}?format=${format}`, {
      headers: {
        ...this.getAuthHeaders(),
        'Accept': format === 'csv' ? 'text/csv' : 'application/json',
      },
    });
  }

  async createBackup() {
    return this.makeRequest('/backup', {
      method: 'POST',
    });
  }

  async restoreBackup(backupId) {
    return this.makeRequest(`/backup/${backupId}/restore`, {
      method: 'POST',
    });
  }

  async getBackups() {
    return this.makeRequest('/backup');
  }
}

// Create singleton instance
const apiService = new ApiService();

// Export both the class and the instance
export { ApiService, ApiError };
export default apiService;

// Utility functions for common operations
export const withRetry = async (operation, maxRetries = 3, delay = 1000) => {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === maxRetries || error.status === 401) {
        throw error;
      }
      
      console.warn(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
      delay *= 2; // Exponential backoff
    }
  }
};

export const handleApiError = (error, customHandlers = {}) => {
  if (error instanceof ApiError) {
    const handler = customHandlers[error.status];
    if (handler) {
      return handler(error);
    }
    
    switch (error.status) {
      case 401:
        console.error('Authentication required');
        // Redirect to login
        window.location.href = '/login';
        break;
      case 403:
        console.error('Access forbidden');
        break;
      case 404:
        console.error('Resource not found');
        break;
      case 429:
        console.error('Rate limit exceeded');
        break;
      case 500:
        console.error('Server error');
        break;
      default:
        console.error('API error:', error.message);
    }
  } else {
    console.error('Network error:', error.message);
  }
};
