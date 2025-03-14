import React, { useEffect, useState } from 'react';
import { Row, Col, Spin, DatePicker, message, Alert } from 'antd';
import {
  DollarOutlined,
  TeamOutlined,
  ProjectOutlined,
  ClockCircleOutlined,
} from '@ant-design/icons';
import dayjs from 'dayjs';

import MetricsCard from '../components/dashboard/MetricsCard';
import ProjectHealthChart from '../components/dashboard/ProjectHealthChart';
import ResourceUtilization from '../components/dashboard/ResourceUtilization';
import dashboardService from '../services/dashboard.service';
import { DashboardMetrics } from '../types';

const { RangePicker } = DatePicker;

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [projectHealth, setProjectHealth] = useState<any[]>([]);
  const [resources, setResources] = useState<any[]>([]);
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().subtract(30, 'days'),
    dayjs(),
  ]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [metricsData, healthData, resourceData] = await Promise.all([
        dashboardService.getMetrics(),
        dashboardService.getProjectHealthMetrics(),
        dashboardService.getResourceUtilization({
          start_date: dateRange[0].format('YYYY-MM-DD'),
          end_date: dateRange[1].format('YYYY-MM-DD'),
        }),
      ]);

      setMetrics(metricsData);
      setProjectHealth(healthData);
      setResources(resourceData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setError('Failed to fetch dashboard data. Please try again later.');
      message.error('Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [dateRange]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ margin: 0 }}>Dashboard</h1>
        <RangePicker
          value={dateRange}
          onChange={(dates) => dates && setDateRange(dates)}
        />
      </div>

      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <MetricsCard
            title="Total Revenue"
            value={metrics?.revenue || 0}
            prefix={<DollarOutlined />}
            trend={{ value: metrics?.revenueTrend || 0, isPositive: (metrics?.revenueTrend || 0) > 0 }}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <MetricsCard
            title="Active Projects"
            value={metrics?.activeProjects || 0}
            prefix={<ProjectOutlined />}
            trend={{ value: metrics?.projectsTrend || 0, isPositive: (metrics?.projectsTrend || 0) > 0 }}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <MetricsCard
            title="Team Members"
            value={metrics?.teamMembers || 0}
            prefix={<TeamOutlined />}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <MetricsCard
            title="Avg. Utilization"
            value={metrics?.avgUtilization || 0}
            suffix="%"
            prefix={<ClockCircleOutlined />}
            trend={{ value: metrics?.utilizationTrend || 0, isPositive: (metrics?.utilizationTrend || 0) > 0 }}
          />
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={14}>
          <ProjectHealthChart data={projectHealth} />
        </Col>
        <Col xs={24} lg={10}>
          <ResourceUtilization data={resources} />
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
