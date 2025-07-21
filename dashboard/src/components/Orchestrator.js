import React, { useState, useEffect } from 'react';
import {
  ThunderboltOutlined,
  SettingOutlined,
  BarChartOutlined,
  ApiOutlined,
  BranchesOutlined,
  ClusterOutlined,
  RocketOutlined,
  TrophyOutlined,
  AlertOutlined,
  CheckCircleOutlined,
  LoadingOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  ReloadOutlined,
  DownloadOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  EyeOutlined
} from '@ant-design/icons';
import { apiService } from '../services/api';

// Orchestrator Task Card Component
const TaskCard = ({ task, onViewDetails }) => (
  <div className="glass-card fade-in">
    <div className="card-header">
      <div className="task-info">
        <h3 className="task-title">{task.objective}</h3>
        <span className={`task-status status-${task.status.toLowerCase()}`}>
          {task.status === 'running' && <LoadingOutlined spin />}
          {task.status === 'completed' && <CheckCircleOutlined />}
          {task.status === 'failed' && <AlertOutlined />}
          {task.status}
        </span>
      </div>
      <button 
        className="btn btn-secondary"
        onClick={() => onViewDetails(task.id)}
      >
        <EyeOutlined />
        Details
      </button>
    </div>
    
    <div className="task-metrics">
      <div className="task-metric">
        <div className="metric-value">{task.progress || 0}%</div>
        <div className="metric-label">Progress</div>
      </div>
      <div className="task-metric">
        <div className="metric-value">{task.agents_count || 0}</div>
        <div className="metric-label">Agents</div>
      </div>
      <div className="task-metric">
        <div className="metric-value">{task.duration || 0}s</div>
        <div className="metric-label">Duration</div>
      </div>
    </div>
    
    {task.progress && (
      <div className="progress-bar" style={{ marginTop: '16px' }}>
        <div className="progress-fill" style={{ width: `${task.progress}%` }}></div>
      </div>
    )}
  </div>
);

// Resource Usage Component
const ResourceUsage = ({ resources }) => (
  <div className="glass-card">
    <div className="card-header">
      <h3 className="card-title">Resource Utilization</h3>
      <ReloadOutlined className="reload-icon" />
    </div>
    
    <div className="resource-list">
      {Object.entries(resources).map(([resourceType, data]) => (
        <div key={resourceType} className="resource-item">
          <div className="resource-header">
            <span className="resource-name">{resourceType.toUpperCase()}</span>
            <span className="resource-value">
              {data.utilization_percent.toFixed(1)}%
            </span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ 
                width: `${data.utilization_percent}%`,
                backgroundColor: data.utilization_percent > 80 ? '#ff4d4f' : 
                                data.utilization_percent > 60 ? '#faad14' : '#52c41a'
              }}
            ></div>
          </div>
          <div className="resource-details">
            <span>Available: {data.available_capacity.toFixed(1)} {data.unit || 'units'}</span>
            <span>Active: {data.active_allocations}</span>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// Performance Metrics Component
const PerformanceMetrics = ({ metrics }) => (
  <div className="glass-card">
    <div className="card-header">
      <h3 className="card-title">Performance Analytics</h3>
      <span className={`performance-score ${
        metrics.performance_score > 80 ? 'excellent' : 
        metrics.performance_score > 60 ? 'good' : 'needs-attention'
      }`}>
        {metrics.performance_score}/100
      </span>
    </div>
    
    <div className="performance-grid">
      <div className="perf-metric">
        <div className="perf-icon">
          <ThunderboltOutlined />
        </div>
        <div className="perf-content">
          <div className="perf-value">{metrics.recent_performance_score}/100</div>
          <div className="perf-label">System Score</div>
        </div>
      </div>
      
      <div className="perf-metric">
        <div className="perf-icon">
          <AlertOutlined />
        </div>
        <div className="perf-content">
          <div className="perf-value">{metrics.active_alerts}</div>
          <div className="perf-label">Active Alerts</div>
        </div>
      </div>
      
      <div className="perf-metric">
        <div className="perf-icon">
          <BarChartOutlined />
        </div>
        <div className="perf-content">
          <div className="perf-value">{metrics.total_analyses}</div>
          <div className="perf-label">Analyses</div>
        </div>
      </div>
    </div>
    
    {metrics.performance_trend && (
      <div className="trend-indicator">
        {metrics.performance_trend === 'improving' ? (
          <ArrowUpOutlined className="trend-up" />
        ) : (
          <ArrowDownOutlined className="trend-down" />
        )}
        Performance {metrics.performance_trend}
      </div>
    )}
  </div>
);

// Intelligence Coordination Component
const IntelligenceCoordination = ({ patterns }) => (
  <div className="glass-card">
    <div className="card-header">
      <h3 className="card-title">Intelligence Coordination</h3>
      <ClusterOutlined />
    </div>
    
    <div className="coordination-stats">
      <div className="coord-stat">
        <div className="stat-value">{patterns.total_coordinations || 0}</div>
        <div className="stat-label">Total Coordinations</div>
      </div>
      
      <div className="coord-stat">
        <div className="stat-value">{patterns.successful_coordinations || 0}</div>
        <div className="stat-label">Successful</div>
      </div>
      
      <div className="coord-stat">
        <div className="stat-value">{patterns.registered_agents || 0}</div>
        <div className="stat-label">Registered Agents</div>
      </div>
    </div>
    
    {patterns.strategy_effectiveness && (
      <div className="strategy-effectiveness">
        <h4>Strategy Effectiveness</h4>
        {Object.entries(patterns.strategy_effectiveness).map(([strategy, effectiveness]) => (
          <div key={strategy} className="strategy-item">
            <span className="strategy-name">{strategy}</span>
            <div className="strategy-bar">
              <div 
                className="strategy-fill" 
                style={{ width: `${effectiveness * 100}%` }}
              ></div>
            </div>
            <span className="strategy-value">{(effectiveness * 100).toFixed(1)}%</span>
          </div>
        ))}
      </div>
    )}
  </div>
);

// Architecture Optimization Component
const ArchitectureOptimization = ({ optimization }) => (
  <div className="glass-card">
    <div className="card-header">
      <h3 className="card-title">Architecture Optimization</h3>
      <BranchesOutlined />
    </div>
    
    {optimization && (
      <>
        <div className="optimization-metrics">
          <div className="opt-metric">
            <div className="opt-value">{optimization.current_metrics?.overall_score?.toFixed(1) || 0}</div>
            <div className="opt-label">Overall Score</div>
          </div>
          
          <div className="opt-metric">
            <div className="opt-value">{optimization.component_count || 0}</div>
            <div className="opt-label">Components</div>
          </div>
          
          <div className="opt-metric">
            <div className="opt-value">{optimization.recommendations?.length || 0}</div>
            <div className="opt-label">Recommendations</div>
          </div>
        </div>
        
        {optimization.bottlenecks && optimization.bottlenecks.length > 0 && (
          <div className="bottlenecks-section">
            <h4>Identified Bottlenecks</h4>
            <div className="bottlenecks-list">
              {optimization.bottlenecks.slice(0, 3).map((bottleneck, index) => (
                <div key={index} className="bottleneck-item">
                  <AlertOutlined className="bottleneck-icon" />
                  <span>{bottleneck}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </>
    )}
  </div>
);

// Create Task Modal Component
const CreateTaskModal = ({ isOpen, onClose, onSubmit }) => {
  const [taskData, setTaskData] = useState({
    objective: '',
    required_capabilities: [],
    strategy: 'hybrid',
    priority: 3,
    timeout: 300
  });

  const [capabilityInput, setCapabilityInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(taskData);
    setTaskData({
      objective: '',
      required_capabilities: [],
      strategy: 'hybrid',
      priority: 3,
      timeout: 300
    });
    onClose();
  };

  const addCapability = () => {
    if (capabilityInput.trim() && !taskData.required_capabilities.includes(capabilityInput.trim())) {
      setTaskData({
        ...taskData,
        required_capabilities: [...taskData.required_capabilities, capabilityInput.trim()]
      });
      setCapabilityInput('');
    }
  };

  const removeCapability = (capability) => {
    setTaskData({
      ...taskData,
      required_capabilities: taskData.required_capabilities.filter(c => c !== capability)
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Create Orchestrated Task</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label>Task Objective</label>
            <textarea
              value={taskData.objective}
              onChange={(e) => setTaskData({...taskData, objective: e.target.value})}
              placeholder="Describe what you want to accomplish..."
              required
              rows={3}
            />
          </div>
          
          <div className="form-group">
            <label>Required Capabilities</label>
            <div className="capability-input">
              <input
                type="text"
                value={capabilityInput}
                onChange={(e) => setCapabilityInput(e.target.value)}
                placeholder="Enter capability and press Add"
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addCapability())}
              />
              <button type="button" onClick={addCapability} className="btn btn-secondary">
                Add
              </button>
            </div>
            <div className="capabilities-list">
              {taskData.required_capabilities.map((capability, index) => (
                <span key={index} className="capability-tag">
                  {capability}
                  <button 
                    type="button" 
                    onClick={() => removeCapability(capability)}
                    className="capability-remove"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>
          
          <div className="form-row">
            <div className="form-group">
              <label>Strategy</label>
              <select
                value={taskData.strategy}
                onChange={(e) => setTaskData({...taskData, strategy: e.target.value})}
              >
                <option value="hybrid">Hybrid</option>
                <option value="sequential">Sequential</option>
                <option value="parallel">Parallel</option>
                <option value="hierarchical">Hierarchical</option>
                <option value="consensus">Consensus</option>
              </select>
            </div>
            
            <div className="form-group">
              <label>Priority</label>
              <select
                value={taskData.priority}
                onChange={(e) => setTaskData({...taskData, priority: parseInt(e.target.value)})}
              >
                <option value={1}>Critical</option>
                <option value={2}>High</option>
                <option value={3}>Medium</option>
                <option value={4}>Low</option>
                <option value={5}>Background</option>
              </select>
            </div>
          </div>
          
          <div className="form-group">
            <label>Timeout (seconds)</label>
            <input
              type="number"
              value={taskData.timeout}
              onChange={(e) => setTaskData({...taskData, timeout: parseInt(e.target.value)})}
              min={30}
              max={3600}
            />
          </div>
          
          <div className="modal-actions">
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              <RocketOutlined />
              Create Task
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Main Orchestrator Component
const Orchestrator = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [orchestratorStatus, setOrchestratorStatus] = useState(null);
  const [activeTasks, setActiveTasks] = useState([]);
  const [resourceStatus, setResourceStatus] = useState({});
  const [performanceMetrics, setPerformanceMetrics] = useState({});
  const [coordinationPatterns, setCoordinationPatterns] = useState({});
  const [architectureOptimization, setArchitectureOptimization] = useState(null);
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadOrchestratorData();
    const interval = setInterval(loadOrchestratorData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadOrchestratorData = async () => {
    try {
      setLoading(true);
      
      // Load orchestrator status
      const statusResponse = await apiService.get('/api/orchestrator/status');
      setOrchestratorStatus(statusResponse.data);
      
      if (statusResponse.data.resource_status) {
        setResourceStatus(statusResponse.data.resource_status.resource_utilization || {});
      }
      
      if (statusResponse.data.performance_insights) {
        setPerformanceMetrics(statusResponse.data.performance_insights);
      }
      
      // Load coordination patterns
      try {
        const patternsResponse = await apiService.get('/api/orchestrator/intelligence/patterns');
        setCoordinationPatterns(patternsResponse.data);
      } catch (error) {
        console.warn('Could not load coordination patterns:', error);
      }
      
    } catch (error) {
      console.error('Failed to load orchestrator data:', error);
    } finally {
      setLoading(false);
    }
  };

  const createOrchestratedTask = async (taskData) => {
    try {
      const response = await apiService.post('/api/orchestrator/tasks', taskData);
      console.log('Task created:', response.data);
      
      // Add to active tasks list
      setActiveTasks(prev => [...prev, {
        id: response.data.task_id,
        objective: taskData.objective,
        status: 'running',
        progress: 0,
        agents_count: 0,
        duration: 0
      }]);
      
      // Reload data to get updated status
      setTimeout(loadOrchestratorData, 1000);
    } catch (error) {
      console.error('Failed to create task:', error);
      alert('Failed to create task. Please try again.');
    }
  };

  const optimizeArchitecture = async () => {
    try {
      setLoading(true);
      const response = await apiService.get('/api/orchestrator/architecture/optimize');
      setArchitectureOptimization(response.data);
    } catch (error) {
      console.error('Failed to optimize architecture:', error);
      alert('Failed to optimize architecture. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const performanceAnalysis = async () => {
    try {
      setLoading(true);
      const response = await apiService.post('/api/orchestrator/performance/analyze', {
        analysis_type: 'real_time',
        time_range_hours: 1
      });
      console.log('Performance analysis completed:', response.data);
      
      // Reload performance data
      const insightsResponse = await apiService.get('/api/orchestrator/performance/insights');
      setPerformanceMetrics(insightsResponse.data);
    } catch (error) {
      console.error('Failed to perform analysis:', error);
      alert('Failed to perform analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { key: 'overview', label: 'Overview', icon: <DashboardOutlined /> },
    { key: 'tasks', label: 'Tasks', icon: <RocketOutlined /> },
    { key: 'resources', label: 'Resources', icon: <SettingOutlined /> },
    { key: 'performance', label: 'Performance', icon: <BarChartOutlined /> },
    { key: 'intelligence', label: 'Intelligence', icon: <ClusterOutlined /> }
  ];

  return (
    <div className="main-content">
      <div className="page-header">
        <h1 className="text-gradient">AI Orchestrator</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
          Advanced intelligence coordination and system optimization
        </p>
        
        <div className="page-actions">
          <button 
            className="btn btn-primary"
            onClick={() => setIsTaskModalOpen(true)}
          >
            <RocketOutlined />
            Create Task
          </button>
          <button 
            className="btn btn-secondary"
            onClick={optimizeArchitecture}
            disabled={loading}
          >
            <BranchesOutlined />
            Optimize Architecture
          </button>
          <button 
            className="btn btn-secondary"
            onClick={performanceAnalysis}
            disabled={loading}
          >
            <BarChartOutlined />
            Analyze Performance
          </button>
        </div>
      </div>

      <div className="tab-navigation">
        {tabs.map(tab => (
          <button
            key={tab.key}
            className={`tab-button ${activeTab === tab.key ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.key)}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {loading && (
        <div className="loading-container">
          <LoadingOutlined spin style={{ fontSize: '32px' }} />
          <p>Loading orchestrator data...</p>
        </div>
      )}

      {/* Overview Tab */}
      {activeTab === 'overview' && !loading && (
        <div className="orchestrator-grid">
          <div className="grid-section">
            <div className="section-header">
              <h3>System Status</h3>
              {orchestratorStatus && (
                <div className="status-indicators">
                  {Object.entries(orchestratorStatus).slice(0, 4).map(([service, status]) => (
                    <div key={service} className={`status-indicator ${status ? 'active' : 'inactive'}`}>
                      <div className="status-dot"></div>
                      {service.replace('_', ' ')}
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            <div className="overview-cards">
              <ResourceUsage resources={resourceStatus} />
              <PerformanceMetrics metrics={performanceMetrics} />
            </div>
          </div>
          
          <div className="grid-section">
            <IntelligenceCoordination patterns={coordinationPatterns} />
            {architectureOptimization && (
              <ArchitectureOptimization optimization={architectureOptimization} />
            )}
          </div>
        </div>
      )}

      {/* Tasks Tab */}
      {activeTab === 'tasks' && !loading && (
        <div className="tasks-container">
          <div className="tasks-header">
            <h3>Active Tasks</h3>
            <span className="task-count">{activeTasks.length} active</span>
          </div>
          
          <div className="tasks-grid">
            {activeTasks.length > 0 ? (
              activeTasks.map(task => (
                <TaskCard 
                  key={task.id} 
                  task={task} 
                  onViewDetails={(id) => console.log('View details for:', id)}
                />
              ))
            ) : (
              <div className="empty-state">
                <RocketOutlined className="empty-icon" />
                <h3>No Active Tasks</h3>
                <p>Create a new orchestrated task to get started</p>
                <button 
                  className="btn btn-primary"
                  onClick={() => setIsTaskModalOpen(true)}
                >
                  Create Task
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Resources Tab */}
      {activeTab === 'resources' && !loading && (
        <div className="resources-container">
          <ResourceUsage resources={resourceStatus} />
        </div>
      )}

      {/* Performance Tab */}
      {activeTab === 'performance' && !loading && (
        <div className="performance-container">
          <PerformanceMetrics metrics={performanceMetrics} />
        </div>
      )}

      {/* Intelligence Tab */}
      {activeTab === 'intelligence' && !loading && (
        <div className="intelligence-container">
          <IntelligenceCoordination patterns={coordinationPatterns} />
        </div>
      )}

      <CreateTaskModal
        isOpen={isTaskModalOpen}
        onClose={() => setIsTaskModalOpen(false)}
        onSubmit={createOrchestratedTask}
      />
    </div>
  );
};

export default Orchestrator;
