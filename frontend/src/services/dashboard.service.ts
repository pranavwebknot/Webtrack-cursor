import api from './api';
import { DashboardMetrics, ProjectFinancials } from '../types';

// Mock data for initial testing
const mockData = {
  metrics: {
    revenue: 150000,
    revenueTrend: 15,
    activeProjects: 12,
    projectsTrend: 8,
    teamMembers: 25,
    avgUtilization: 85,
    utilizationTrend: 5,
  },
  projectHealth: [
    {
      name: 'Q1 2024',
      onTrack: 8,
      atRisk: 3,
      delayed: 1,
    },
    {
      name: 'Q2 2024',
      onTrack: 10,
      atRisk: 2,
      delayed: 2,
    },
    {
      name: 'Q3 2024',
      onTrack: 7,
      atRisk: 4,
      delayed: 1,
    },
  ],
  resourceUtilization: [
    {
      id: 1,
      name: 'John Doe',
      department: 'Development',
      utilization: 90,
      projects: ['Project A', 'Project B'],
    },
    {
      id: 2,
      name: 'Jane Smith',
      department: 'Design',
      utilization: 75,
      projects: ['Project C'],
    },
    {
      id: 3,
      name: 'Mike Johnson',
      department: 'Development',
      utilization: 85,
      projects: ['Project A', 'Project D'],
    },
  ],
};

class DashboardService {
  // General Metrics
  async getMetrics(): Promise<DashboardMetrics> {
    try {
      const response = await api.get<DashboardMetrics>('/api/dashboard/metrics/');
      return response.data;
    } catch (error) {
      console.warn('Using mock data for metrics:', error);
      return mockData.metrics;
    }
  }

  // Project Health
  async getProjectHealthMetrics() {
    try {
      const response = await api.get('/api/dashboard/project-health/');
      return response.data;
    } catch (error) {
      console.warn('Using mock data for project health:', error);
      return mockData.projectHealth;
    }
  }

  // Financial Metrics
  async getFinancialMetrics(params?: {
    start_date?: string;
    end_date?: string;
    project?: number;
  }) {
    try {
      const response = await api.get<ProjectFinancials[]>('/api/dashboard/financials/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching financial metrics:', error);
      throw error;
    }
  }

  // Resource Utilization
  async getResourceUtilization(params?: {
    department?: string;
    start_date?: string;
    end_date?: string;
  }) {
    try {
      const response = await api.get('/api/dashboard/resource-utilization/', { params });
      return response.data;
    } catch (error) {
      console.warn('Using mock data for resource utilization:', error);
      return mockData.resourceUtilization;
    }
  }

  // Performance Overview
  async getPerformanceOverview(params?: {
    department?: string;
    period?: string;
  }) {
    try {
      const response = await api.get('/api/dashboard/performance-overview/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching performance overview:', error);
      throw error;
    }
  }

  // Leave Statistics
  async getLeaveStatistics(params?: {
    department?: string;
    year?: number;
  }) {
    try {
      const response = await api.get('/api/dashboard/leave-statistics/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching leave statistics:', error);
      throw error;
    }
  }

  // Timesheet Summary
  async getTimesheetSummary(params?: {
    department?: string;
    start_date?: string;
    end_date?: string;
  }) {
    try {
      const response = await api.get('/api/dashboard/timesheet-summary/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching timesheet summary:', error);
      throw error;
    }
  }

  // Project Profitability
  async getProjectProfitability(params?: {
    start_date?: string;
    end_date?: string;
  }) {
    try {
      const response = await api.get('/api/dashboard/project-profitability/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching project profitability:', error);
      throw error;
    }
  }

  // Team Allocation
  async getTeamAllocation(params?: {
    department?: string;
    date?: string;
  }) {
    try {
      const response = await api.get('/api/dashboard/team-allocation/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching team allocation:', error);
      throw error;
    }
  }

  // Upcoming Reviews
  async getUpcomingReviews() {
    const response = await api.get('/dashboards/upcoming-reviews/');
    return response.data;
  }

  // Pending Approvals
  async getPendingApprovals() {
    const response = await api.get('/dashboards/pending-approvals/');
    return response.data;
  }

  // Export Reports
  async exportReport(reportType: string, params?: {
    format?: 'pdf' | 'excel';
    start_date?: string;
    end_date?: string;
    department?: string;
  }) {
    const response = await api.get(`/dashboards/export/${reportType}/`, {
      params,
      responseType: 'blob',
    });
    return response.data;
  }
}

export default new DashboardService();
