import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Menu, Typography, Card, Row, Col, Statistic } from 'antd';
import {
  DashboardOutlined,
  RobotOutlined,
  FileTextOutlined,
  SettingOutlined,
  SecurityScanOutlined,
  BarChartOutlined
} from '@ant-design/icons';
import './App.css';

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

// Dashboard Overview Component
const Dashboard = () => {
  return (
    <div>
      <Title level={2}>AI Operating System Dashboard</Title>
      <Row gutter={16} style={{ marginBottom: 20 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Active Agents"
              value={9}
              prefix={<RobotOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Reports Generated"
              value={12}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Security Score"
              value={85}
              suffix="%"
              prefix={<SecurityScanOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="System Health"
              value={92}
              suffix="%"
              prefix={<BarChartOutlined />}
            />
          </Card>
        </Col>
      </Row>
      
      <Card title="Recent Agent Activity" style={{ marginBottom: 20 }}>
        <p>✅ CostOptBot: Identified $630 in potential savings</p>
        <p>✅ SecuBot: Completed security scan - 3 issues found</p>
        <p>✅ PrivacyGuard: GDPR compliance check completed</p>
        <p>✅ InsightsBot: Generated executive dashboard</p>
      </Card>
      
      <Card title="Quick Actions">
        <p>🚀 Run all agents</p>
        <p>🔒 Execute security suite</p>
        <p>📊 Generate reports</p>
        <p>⚙️ System configuration</p>
      </Card>
    </div>
  );
};

// Agents Component
const Agents = () => {
  const agents = [
    { name: 'CostOptBot', role: 'Cost Optimization', status: 'Active' },
    { name: 'ComplianceBot', role: 'Compliance Auditing', status: 'Active' },
    { name: 'TestGenie', role: 'Testing Automation', status: 'Active' },
    { name: 'SecuBot', role: 'Security Hardening', status: 'Active' },
    { name: 'PrivacyGuard', role: 'Data Privacy', status: 'Active' },
    { name: 'InsightsBot', role: 'Analytics & Insights', status: 'Active' },
    { name: 'ConvDesignBot', role: 'Conversation Design', status: 'Active' },
    { name: 'ModelRefactor', role: 'Code Refactoring', status: 'Active' },
    { name: 'ArchitectureDesignerAgent', role: 'Architecture Design', status: 'Active' }
  ];

  return (
    <div>
      <Title level={2}>AI Agents</Title>
      <Row gutter={[16, 16]}>
        {agents.map((agent, index) => (
          <Col span={8} key={index}>
            <Card title={agent.name} extra={<span style={{ color: 'green' }}>●</span>}>
              <p><strong>Role:</strong> {agent.role}</p>
              <p><strong>Status:</strong> {agent.status}</p>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

// Reports Component
const Reports = () => {
  return (
    <div>
      <Title level={2}>Generated Reports</Title>
      <Card title="Available Reports">
        <p>📄 Cost Optimization Report</p>
        <p>📄 Security Analysis Report</p>
        <p>📄 Compliance Audit Report</p>
        <p>📄 Privacy Assessment Report</p>
        <p>📄 System Insights Report</p>
        <p>📄 Architecture Design Document</p>
        <p>📄 Refactoring Plan</p>
        <p>📄 Testing Report</p>
        <p>📄 Executive Dashboard</p>
      </Card>
    </div>
  );
};

// Settings Component
const Settings = () => {
  return (
    <div>
      <Title level={2}>System Settings</Title>
      <Card title="Configuration">
        <p>🔧 Agent Configuration</p>
        <p>🔧 System Parameters</p>
        <p>🔧 Reporting Settings</p>
        <p>🔧 Security Policies</p>
      </Card>
    </div>
  );
};

function App() {
  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '2',
      icon: <RobotOutlined />,
      label: 'Agents',
    },
    {
      key: '3',
      icon: <FileTextOutlined />,
      label: 'Reports',
    },
    {
      key: '4',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
  ];

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider theme="dark">
          <div style={{ padding: '16px', color: 'white', textAlign: 'center' }}>
            <Title level={4} style={{ color: 'white', margin: 0 }}>AIMOS</Title>
          </div>
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']} items={menuItems} />
        </Sider>
        <Layout>
          <Header style={{ background: '#fff', padding: '0 24px' }}>
            <Title level={3} style={{ margin: 0, lineHeight: '64px' }}>
              AI Operating System Framework
            </Title>
          </Header>
          <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/agents" element={<Agents />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Router>
  );
}

export default App;
