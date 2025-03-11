import api from './api';
import { DashboardMetrics, ProjectFinancials } from '../types';

class DashboardService {
  // General Metrics
  async getMetrics(): Promise<DashboardMetrics> {
    const response = await api.get<DashboardMetrics>('/dashboards/metrics/');
    return response.data;
  }

  // Project Health
  async getProjectHealthMetrics() {
    const response = await api.get('/dashboards/project-health/');
    return response.data;
  }

  // Financial Metrics
  async getFinancialMetrics(params?: {
    start_date?: string;
    end_date?: string;
    project?: number;
  }) {
    const response = await api.get<ProjectFinancials[]>('/dashboards/financials/', { params });
    return response.data;
  }

  // Resource Utilization
  async getResourceUtilization(params?: {
    department?: string;
    start_date?: string;
    end_date?: string;
  }) {
    const response = await api.get('/dashboards/resource-utilization/', { params });
    return response.data;
  }

  // Performance Overview
  async getPerformanceOverview(params?: {
    department?: string;
    period?: string;
  }) {
    const response = await api.get('/dashboards/performance-overview/', { params });
    return response.data;
  }

  // Leave Statistics
  async getLeaveStatistics(params?: {
    department?: string;
    year?: number;
  }) {
    const response = await api.get('/dashboards/leave-statistics/', { params });
    return response.data;
  }

  // Timesheet Summary
  async getTimesheetSummary(params?: {
    department?: string;
    start_date?: string;
    end_date?: string;
  }) {
    const response = await api.get('/dashboards/timesheet-summary/', { params });
    return response.data;
  }

  // Project Profitability
  async getProjectProfitability(params?: {
    start_date?: string;
    end_date?: string;
  }) {
    const response = await api.get('/dashboards/project-profitability/', { params });
    return response.data;
  }

  // Team Allocation
  async getTeamAllocation(params?: {
    department?: string;
    date?: string;
  }) {
    const response = await api.get('/dashboards/team-allocation/', { params });
    return response.data;
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
