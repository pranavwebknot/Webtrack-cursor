import React, { useState } from 'react';
import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  ClockCircleOutlined,
  CalendarOutlined,
  TrophyOutlined,
  TeamOutlined,
  ProjectOutlined,
  FileTextOutlined,
} from '@ant-design/icons';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import Header from '../components/Header';
import theme from '../theme';
import WebknotLogo from '../components/WebknotLogo';

const { Sider, Content } = Layout;

const MainLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/timesheet',
      icon: <ClockCircleOutlined />,
      label: 'Timesheet',
    },
    {
      key: '/leave',
      icon: <CalendarOutlined />,
      label: 'Leave',
    },
    {
      key: '/performance',
      icon: <TrophyOutlined />,
      label: 'Performance',
    },
    {
      key: '/projects',
      icon: <ProjectOutlined />,
      label: 'Projects',
    },
    {
      key: '/team',
      icon: <TeamOutlined />,
      label: 'Team',
    },
    {
      key: '/reports',
      icon: <FileTextOutlined />,
      label: 'Reports',
    },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        style={{
          background: '#fff',
          boxShadow: theme.shadows.sm,
        }}
      >
        <div style={{
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          borderBottom: '1px solid #f0f0f0',
          padding: '0 16px',
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            cursor: 'pointer',
          }} onClick={() => navigate('/')}>
            <WebknotLogo width={32} height={32} />
            {!collapsed && (
              <span style={{
                fontSize: '16px',
                fontWeight: 700,
                letterSpacing: '1px',
                color: theme.colors.brand.purple,
                whiteSpace: 'nowrap',
              }}>
                WEBKNOT
              </span>
            )}
          </div>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{
            borderRight: 0,
          }}
        />
      </Sider>
      <Layout>
        <Header
          collapsed={collapsed}
          onToggle={() => setCollapsed(!collapsed)}
        />
        <Content
          style={{
            margin: '24px',
            padding: '24px',
            background: '#fff',
            borderRadius: theme.borderRadius.lg,
            minHeight: 280,
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
