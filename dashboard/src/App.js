import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  RobotOutlined,
  FileTextOutlined,
  SettingOutlined,
  SecurityScanOutlined,
  BarChartOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  ReloadOutlined,
  UserOutlined,
  BellOutlined,
  SearchOutlined,
  MenuOutlined,
  CloseOutlined,
  TrophyOutlined,
  ThunderboltOutlined,
  EyeOutlined,
  DownloadOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  ApiOutlined
} from '@ant-design/icons';
import './App.css';
import Orchestrator from './components/Orchestrator';

// Navigation Component
const Navigation = ({ isOpen, toggleSidebar }) => {
  const location = useLocation();
  
  const navigationItems = [
    { key: '/', icon: <DashboardOutlined />, label: 'Dashboard' },
    { key: '/orchestrator', icon: <ApiOutlined />, label: 'Orchestrator' },
    { key: '/agents', icon: <RobotOutlined />, label: 'AI Agents' },
    { key: '/reports', icon: <FileTextOutlined />, label: 'Reports' },
    { key: '/security', icon: <SecurityScanOutlined />, label: 'Security' },
    { key: '/settings', icon: <SettingOutlined />, label: 'Settings' },
  ];

  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <h1 className="sidebar-logo">AIMOS</h1>
        <p className="sidebar-subtitle">AI Operating System</p>
      </div>
      
      <nav className="nav-menu">
        {navigationItems.map((item) => (
          <Link
            key={item.key}
            to={item.key}
            className={`nav-item ${location.pathname === item.key ? 'active' : ''}`}
            onClick={() => window.innerWidth <= 768 && toggleSidebar()}
          >
            <span className="nav-icon">{item.icon}</span>
            <span className="nav-label">{item.label}</span>
          </Link>
        ))}
      </nav>
    </div>
  );
};

// Header Component
const Header = ({ toggleSidebar, toggleTheme, currentTheme }) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="main-header">
      <div className="header-left">
        <button 
          className="btn btn-secondary mobile-menu-toggle"
          onClick={toggleSidebar}
          style={{ display: 'none' }}
        >
          <MenuOutlined />
        </button>
        <h2 className="header-title">AI Operating System</h2>
      </div>
      
      <div className="header-actions">
        <div className="header-time">
          {currentTime.toLocaleTimeString()}
        </div>
        <button className="btn btn-secondary">
          <SearchOutlined />
        </button>
        <button className="btn btn-secondary">
          <BellOutlined />
        </button>
        <button className="btn btn-secondary" onClick={toggleTheme}>
          {currentTheme === 'light' ? '🌙' : '☀️'}
        </button>
        <button className="btn btn-secondary">
          <UserOutlined />
        </button>
      </div>
    </header>
  );
};

// Statistics Card Component
const StatCard = ({ icon, value, label, change, trend }) => (
  <div className="stat-card fade-in">
    <div className="stat-icon">{icon}</div>
    <div className="stat-value">{value}</div>
    <div className="stat-label">{label}</div>
    {change && (
      <div className={`stat-change ${trend}`}>
        {trend === 'positive' ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
        {change}
      </div>
    )}
  </div>
);

// Agent Card Component
const AgentCard = ({ agent, onToggle, onView }) => (
  <div className="agent-card fade-in">
    <div className="agent-header">
      <h3 className="agent-name">{agent.name}</h3>
      <span className={`agent-status ${agent.status.toLowerCase()}`}>
        {agent.status}
      </span>
    </div>
    
    <p className="agent-role">{agent.role}</p>
    
    <div className="agent-metrics">
      <div className="agent-metric">
        <div className="metric-value">{agent.successRate}%</div>
        <div className="metric-label">Success</div>
      </div>
      <div className="agent-metric">
        <div className="metric-value">{agent.executions}</div>
        <div className="metric-label">Runs</div>
      </div>
      <div className="agent-metric">
        <div className="metric-value">{agent.uptime}%</div>
        <div className="metric-label">Uptime</div>
      </div>
    </div>
    
    <div className="agent-actions" style={{ marginTop: '16px', display: 'flex', gap: '8px' }}>
      <button 
        className="btn btn-primary"
        onClick={() => onToggle(agent.id)}
      >
        {agent.status === 'Active' ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
        {agent.status === 'Active' ? 'Pause' : 'Start'}
      </button>
      <button 
        className="btn btn-secondary"
        onClick={() => onView(agent.id)}
      >
        <EyeOutlined />
        View
      </button>
    </div>
  </div>
);

// Activity Item Component
const ActivityItem = ({ icon, title, description, time, status = 'success' }) => (
  <div className={`activity-item ${status}`}>
    <div className="activity-icon">{icon}</div>
    <div className="activity-content">
      <div className="activity-title">{title}</div>
      <div className="activity-description">{description}</div>
      <div className="activity-time">{time}</div>
    </div>
  </div>
);

// Quick Action Component
const QuickAction = ({ icon, title, description, onClick }) => (
  <div className="quick-action" onClick={onClick}>
    <div className="quick-action-icon">{icon}</div>
    <div className="quick-action-title">{title}</div>
    <div className="quick-action-description">{description}</div>
  </div>
);

// Dashboard Component
const Dashboard = () => {
  const [systemMetrics, setSystemMetrics] = useState({
    activeAgents: 9,
    reportsGenerated: 23,
    securityScore: 94,
    systemHealth: 98
  });

  const recentActivities = [
    {
      icon: <TrophyOutlined />,
      title: 'CostOptBot Analysis Complete',
      description: 'Identified $2,340 in potential monthly savings across cloud infrastructure',
      time: '2 minutes ago',
      status: 'success'
    },
    {
      icon: <SecurityScanOutlined />,
      title: 'Security Scan Completed',
      description: 'SecuBot detected and resolved 3 minor vulnerabilities',
      time: '5 minutes ago',
      status: 'success'
    },
    {
      icon: <ThunderboltOutlined />,
      title: 'System Performance Optimized',
      description: 'InsightsBot improved query performance by 23%',
      time: '12 minutes ago',
      status: 'success'
    },
    {
      icon: <FileTextOutlined />,
      title: 'Compliance Report Generated',
      description: 'GDPR and SOC2 compliance verification completed successfully',
      time: '18 minutes ago',
      status: 'success'
    }
  ];

  const quickActions = [
    {
      icon: <PlayCircleOutlined />,
      title: 'Run All Agents',
      description: 'Execute complete system analysis',
      onClick: () => console.log('Running all agents...')
    },
    {
      icon: <SecurityScanOutlined />,
      title: 'Security Suite',
      description: 'Run security-focused agents',
      onClick: () => console.log('Running security suite...')
    },
    {
      icon: <BarChartOutlined />,
      title: 'Generate Reports',
      description: 'Create comprehensive analytics',
      onClick: () => console.log('Generating reports...')
    },
    {
      icon: <SettingOutlined />,
      title: 'System Config',
      description: 'Manage system settings',
      onClick: () => console.log('Opening settings...')
    }
  ];

  return (
    <div className="main-content">
      <div className="page-header">
        <h1>AI Operating System Dashboard</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
          Monitor and manage your intelligent agent ecosystem
        </p>
      </div>

      <div className="stats-grid">
        <StatCard
          icon={<RobotOutlined />}
          value={systemMetrics.activeAgents}
          label="Active Agents"
          change="+2"
          trend="positive"
        />
        <StatCard
          icon={<FileTextOutlined />}
          value={systemMetrics.reportsGenerated}
          label="Reports Generated"
          change="+5"
          trend="positive"
        />
        <StatCard
          icon={<SecurityScanOutlined />}
          value={`${systemMetrics.securityScore}%`}
          label="Security Score"
          change="+3%"
          trend="positive"
        />
        <StatCard
          icon={<BarChartOutlined />}
          value={`${systemMetrics.systemHealth}%`}
          label="System Health"
          change="+1%"
          trend="positive"
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 400px', gap: '24px', marginTop: '32px' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Recent Agent Activity</h3>
            <button className="btn btn-secondary">
              <ReloadOutlined />
              Refresh
            </button>
          </div>
          
          <div className="activity-feed">
            {recentActivities.map((activity, index) => (
              <ActivityItem key={index} {...activity} />
            ))}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">System Overview</h3>
          </div>
          
          <div style={{ marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>CPU Usage</span>
              <span style={{ color: 'var(--text-primary)', fontWeight: '600' }}>34%</span>
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '34%' }}></div>
            </div>
          </div>

          <div style={{ marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Memory Usage</span>
              <span style={{ color: 'var(--text-primary)', fontWeight: '600' }}>67%</span>
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '67%' }}></div>
            </div>
          </div>

          <div style={{ marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Agent Efficiency</span>
              <span style={{ color: 'var(--text-primary)', fontWeight: '600' }}>92%</span>
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '92%' }}></div>
            </div>
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: 'var(--text-secondary)' }}>Network I/O</span>
              <span style={{ color: 'var(--text-primary)', fontWeight: '600' }}>23%</span>
            </div>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '23%' }}></div>
            </div>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '32px' }}>
        <div className="card-header">
          <h3 className="card-title">Quick Actions</h3>
          <p className="card-subtitle">Frequently used system operations</p>
        </div>
        
        <div className="quick-actions">
          {quickActions.map((action, index) => (
            <QuickAction key={index} {...action} />
          ))}
        </div>
      </div>
    </div>
  );
};

// Agents Component
const Agents = () => {
  const [agents, setAgents] = useState([
    {
      id: 1,
      name: 'CostOptBot',
      role: 'Cost Optimization & Analysis',
      status: 'Active',
      successRate: 94,
      executions: 127,
      uptime: 99.2
    },
    {
      id: 2,
      name: 'SecuBot',
      role: 'Security Hardening & Monitoring',
      status: 'Active',
      successRate: 98,
      executions: 89,
      uptime: 99.8
    },
    {
      id: 3,
      name: 'ComplianceBot',
      role: 'Regulatory Compliance Auditing',
      status: 'Active',
      successRate: 91,
      executions: 45,
      uptime: 97.3
    },
    {
      id: 4,
      name: 'TestGenie',
      role: 'Automated Testing & QA',
      status: 'Active',
      successRate: 89,
      executions: 234,
      uptime: 98.7
    },
    {
      id: 5,
      name: 'PrivacyGuard',
      role: 'Data Privacy & Protection',
      status: 'Active',
      successRate: 96,
      executions: 67,
      uptime: 99.1
    },
    {
      id: 6,
      name: 'InsightsBot',
      role: 'Analytics & Business Intelligence',
      status: 'Active',
      successRate: 93,
      executions: 156,
      uptime: 98.9
    },
    {
      id: 7,
      name: 'ConvDesignBot',
      role: 'Conversation Design & UX',
      status: 'Inactive',
      successRate: 87,
      executions: 23,
      uptime: 85.4
    },
    {
      id: 8,
      name: 'ModelRefactor',
      role: 'Code Refactoring & Optimization',
      status: 'Active',
      successRate: 92,
      executions: 78,
      uptime: 97.8
    },
    {
      id: 9,
      name: 'ArchitectureBot',
      role: 'System Architecture Design',
      status: 'Active',
      successRate: 95,
      executions: 34,
      uptime: 99.5
    }
  ]);

  const handleToggleAgent = (agentId) => {
    setAgents(prev => prev.map(agent => 
      agent.id === agentId 
        ? { ...agent, status: agent.status === 'Active' ? 'Inactive' : 'Active' }
        : agent
    ));
  };

  const handleViewAgent = (agentId) => {
    console.log(`Viewing details for agent ${agentId}`);
  };

  return (
    <div className="main-content">
      <div className="page-header">
        <h1>AI Agent Management</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
          Monitor and control your intelligent automation agents
        </p>
      </div>

      <div className="stats-grid" style={{ marginBottom: '32px' }}>
        <StatCard
          icon={<RobotOutlined />}
          value={agents.filter(a => a.status === 'Active').length}
          label="Active Agents"
        />
        <StatCard
          icon={<BarChartOutlined />}
          value={`${Math.round(agents.reduce((acc, a) => acc + a.successRate, 0) / agents.length)}%`}
          label="Avg Success Rate"
        />
        <StatCard
          icon={<ThunderboltOutlined />}
          value={agents.reduce((acc, a) => acc + a.executions, 0)}
          label="Total Executions"
        />
        <StatCard
          icon={<TrophyOutlined />}
          value={`${Math.round(agents.reduce((acc, a) => acc + a.uptime, 0) / agents.length)}%`}
          label="Avg Uptime"
        />
      </div>

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Agent Fleet</h3>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="btn btn-primary">
              <PlayCircleOutlined />
              Start All
            </button>
            <button className="btn btn-secondary">
              <ReloadOutlined />
              Refresh
            </button>
          </div>
        </div>

        <div className="agents-grid">
          {agents.map(agent => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onToggle={handleToggleAgent}
              onView={handleViewAgent}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

// Reports Component
const Reports = () => {
  const reports = [
    {
      id: 1,
      title: 'Cost Optimization Analysis',
      description: 'Comprehensive analysis of infrastructure costs and optimization opportunities',
      type: 'Cost Analysis',
      date: '2024-01-15',
      size: '2.3 MB',
      status: 'Ready'
    },
    {
      id: 2,
      title: 'Security Vulnerability Assessment',
      description: 'Detailed security scan results and remediation recommendations',
      type: 'Security',
      date: '2024-01-15',
      size: '4.7 MB',
      status: 'Ready'
    },
    {
      id: 3,
      title: 'Compliance Audit Report',
      description: 'GDPR, SOC2, and regulatory compliance verification results',
      type: 'Compliance',
      date: '2024-01-14',
      size: '1.8 MB',
      status: 'Ready'
    },
    {
      id: 4,
      title: 'System Performance Insights',
      description: 'Performance metrics, bottlenecks, and optimization recommendations',
      type: 'Performance',
      date: '2024-01-14',
      size: '3.2 MB',
      status: 'Ready'
    },
    {
      id: 5,
      title: 'Privacy Assessment Report',
      description: 'Data privacy compliance and protection analysis',
      type: 'Privacy',
      date: '2024-01-13',
      size: '2.1 MB',
      status: 'Ready'
    },
    {
      id: 6,
      title: 'Architecture Design Document',
      description: 'System architecture analysis and design recommendations',
      type: 'Architecture',
      date: '2024-01-13',
      size: '5.4 MB',
      status: 'Ready'
    },
    {
      id: 7,
      title: 'Executive Dashboard Summary',
      description: 'High-level metrics and KPIs for leadership review',
      type: 'Executive',
      date: '2024-01-12',
      size: '1.2 MB',
      status: 'Ready'
    }
  ];

  return (
    <div className="main-content">
      <div className="page-header">
        <h1>Generated Reports</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
          Access and download AI-generated analysis reports
        </p>
      </div>

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Available Reports</h3>
          <button className="btn btn-primary">
            <FileTextOutlined />
            Generate New Report
          </button>
        </div>

        <div className="reports-list">
          {reports.map(report => (
            <div key={report.id} className="report-item">
              <div className="report-icon">
                <FileTextOutlined />
              </div>
              <div className="report-content">
                <div className="report-title">{report.title}</div>
                <div className="report-meta">
                  {report.description} • {report.type} • {report.date} • {report.size}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button className="btn btn-secondary">
                  <EyeOutlined />
                  View
                </button>
                <button className="btn btn-accent">
                  <DownloadOutlined />
                  Download
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Security Component
const Security = () => {
  return (
    <div className="main-content">
      <div className="page-header">
        <h1>Security Center</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
          Monitor system security and manage threat protection
        </p>
      </div>

      <div className="stats-grid">
        <StatCard
          icon={<SecurityScanOutlined />}
          value="94%"
          label="Security Score"
          change="+2%"
          trend="positive"
        />
        <StatCard
          icon={<ThunderboltOutlined />}
          value="23"
          label="Threats Blocked"
          change="+5"
          trend="positive"
        />
        <StatCard
          icon={<FileTextOutlined />}
          value="0"
          label="Critical Issues"
          change="-3"
          trend="positive"
        />
        <StatCard
          icon={<BarChartOutlined />}
          value="99.8%"
          label="Uptime"
          change="+0.1%"
          trend="positive"
        />
      </div>

      <div className="card" style={{ marginTop: '32px' }}>
        <div className="card-header">
          <h3 className="card-title">Security Operations</h3>
        </div>
        
        <div className="quick-actions">
          <QuickAction
            icon={<SecurityScanOutlined />}
            title="Run Security Scan"
            description="Complete system vulnerability assessment"
            onClick={() => console.log('Running security scan...')}
          />
          <QuickAction
            icon={<ThunderboltOutlined />}
            title="Threat Detection"
            description="Real-time threat monitoring"
            onClick={() => console.log('Opening threat detection...')}
          />
          <QuickAction
            icon={<FileTextOutlined />}
            title="Compliance Check"
            description="Verify regulatory compliance"
            onClick={() => console.log('Running compliance check...')}
          />
          <QuickAction
            icon={<SettingOutlined />}
            title="Security Settings"
            description="Configure security policies"
            onClick={() => console.log('Opening security settings...')}
          />
        </div>
      </div>
    </div>
  );
};

// Settings Component
const Settings = () => {
  const [settings, setSettings] = useState({
    autoRun: true,
    notifications: true,
    darkMode: true,
    analytics: true,
    selfHealing: true,
    voiceAgents: false,
    multiModal: true
  });

  const toggleSetting = (key) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="main-content">
      <div className="page-header">
        <h1>System Settings</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
          Configure system behavior and preferences
        </p>
      </div>

      <div className="settings-grid">
        <div className="card">
          <h3 className="settings-title">
            <SettingOutlined />
            General Settings
          </h3>
          
          <div className="settings-item">
            <span className="settings-label">Auto-run Agents</span>
            <div 
              className={`toggle-switch ${settings.autoRun ? 'active' : ''}`}
              onClick={() => toggleSetting('autoRun')}
            />
          </div>
          
          <div className="settings-item">
            <span className="settings-label">Push Notifications</span>
            <div 
              className={`toggle-switch ${settings.notifications ? 'active' : ''}`}
              onClick={() => toggleSetting('notifications')}
            />
          </div>
          
          <div className="settings-item">
            <span className="settings-label">Dark Mode</span>
            <div 
              className={`toggle-switch ${settings.darkMode ? 'active' : ''}`}
              onClick={() => toggleSetting('darkMode')}
            />
          </div>
        </div>

        <div className="card">
          <h3 className="settings-title">
            <RobotOutlined />
            Agent Features
          </h3>
          
          <div className="settings-item">
            <span className="settings-label">Analytics Collection</span>
            <div 
              className={`toggle-switch ${settings.analytics ? 'active' : ''}`}
              onClick={() => toggleSetting('analytics')}
            />
          </div>
          
          <div className="settings-item">
            <span className="settings-label">Self-Healing</span>
            <div 
              className={`toggle-switch ${settings.selfHealing ? 'active' : ''}`}
              onClick={() => toggleSetting('selfHealing')}
            />
          </div>
          
          <div className="settings-item">
            <span className="settings-label">Voice Agents</span>
            <div 
              className={`toggle-switch ${settings.voiceAgents ? 'active' : ''}`}
              onClick={() => toggleSetting('voiceAgents')}
            />
          </div>
          
          <div className="settings-item">
            <span className="settings-label">Multi-Modal Processing</span>
            <div 
              className={`toggle-switch ${settings.multiModal ? 'active' : ''}`}
              onClick={() => toggleSetting('multiModal')}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// Main App Component
function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [theme, setTheme] = useState('dark'); // Add theme state

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Add theme toggling function
  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    document.body.className = `${theme}-theme`;
  }, [theme]);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setSidebarOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <Router>
      <div className="main-layout">
        <Navigation isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
        
        <div className="main-wrapper">
          <Header toggleSidebar={toggleSidebar} toggleTheme={toggleTheme} currentTheme={theme} />
          
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/orchestrator" element={<Orchestrator />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/security" element={<Security />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
        
        {sidebarOpen && (
          <div 
            className="sidebar-overlay"
            onClick={toggleSidebar}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'rgba(0, 0, 0, 0.5)',
              zIndex: 999,
              display: window.innerWidth <= 768 ? 'block' : 'none'
            }}
          />
        )}
      </div>
    </Router>
  );
}

export default App;
