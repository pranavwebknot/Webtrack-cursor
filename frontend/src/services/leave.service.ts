import api from './api';
import { Leave } from '../types';
import { mockLeaveData } from './mockData';

interface LeaveRequestCreateData {
  leave_type: 'ANNUAL' | 'SICK' | 'PERSONAL' | 'OTHER';
  start_date: string;
  end_date: string;
  reason: string;
}

interface LeaveRequestUpdateData extends Partial<LeaveRequestCreateData> {
  status?: 'PENDING' | 'APPROVED' | 'REJECTED';
}

class LeaveService {
  // Leave Requests
  async getLeaveRequests(params?: {
    user?: number;
    status?: string;
    start_date?: string;
    end_date?: string;
  }) {
    try {
      const response = await api.get<{ results: Leave[] }>('/api/leave-requests/', { params });
      return response.data;
    } catch (error) {
      console.warn('Using mock data for leave requests:', error);
      return { results: mockLeaveData.leaveRequests };
    }
  }

  async getLeaveRequest(id: number) {
    try {
      const response = await api.get<Leave>(`/api/leave-requests/${id}/`);
      return response.data;
    } catch (error) {
      console.warn('Using mock data for leave request:', error);
      return mockLeaveData.leaveRequests.find(l => l.id === id);
    }
  }

  async createLeaveRequest(data: LeaveRequestCreateData) {
    try {
      const response = await api.post<Leave>('/api/leave-requests/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating leave request:', error);
      throw error;
    }
  }

  async updateLeaveRequest(id: number, data: LeaveRequestUpdateData) {
    try {
      const response = await api.patch<Leave>(`/api/leave-requests/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating leave request:', error);
      throw error;
    }
  }

  async deleteLeaveRequest(id: number) {
    try {
      await api.delete(`/api/leave-requests/${id}/`);
    } catch (error) {
      console.error('Error deleting leave request:', error);
      throw error;
    }
  }

  async approveLeaveRequest(id: number) {
    try {
      const response = await api.post<Leave>(`/api/leave-requests/${id}/approve/`);
      return response.data;
    } catch (error) {
      console.error('Error approving leave request:', error);
      throw error;
    }
  }

  async rejectLeaveRequest(id: number, reason: string) {
    try {
      const response = await api.post<Leave>(`/api/leave-requests/${id}/reject/`, { reason });
      return response.data;
    } catch (error) {
      console.error('Error rejecting leave request:', error);
      throw error;
    }
  }

  // Leave Balances
  async getLeaveBalance(userId?: number) {
    try {
      const response = await api.get('/api/leave-balances/', {
        params: userId ? { user: userId } : undefined,
      });
      return response.data;
    } catch (error) {
      console.warn('Using mock data for leave balance:', error);
      return mockLeaveData.leaveBalance;
    }
  }

  // Leave Types
  async getLeaveTypes() {
    try {
      const response = await api.get('/api/leave-types/');
      return response.data;
    } catch (error) {
      console.warn('Using mock data for leave types:', error);
      return {
        results: [
          { id: 1, name: 'Annual Leave', default_days: 20 },
          { id: 2, name: 'Sick Leave', default_days: 10 },
          { id: 3, name: 'Personal Leave', default_days: 5 },
          { id: 4, name: 'Other Leave', default_days: 0 },
        ],
      };
    }
  }

  // Leave Policies
  async getLeavePolicies() {
    try {
      const response = await api.get('/api/leave-policies/');
      return response.data;
    } catch (error) {
      console.error('Error fetching leave policies:', error);
      throw error;
    }
  }

  // Analytics
  async getLeaveAnalytics(params?: {
    department?: string;
    year?: number;
  }) {
    try {
      const response = await api.get('/api/leave-requests/analytics/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching leave analytics:', error);
      throw error;
    }
  }

  async getTeamCalendar(params?: {
    department?: string;
    month?: string;
  }) {
    try {
      const response = await api.get('/api/leave-requests/calendar/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching team calendar:', error);
      throw error;
    }
  }
}

export default new LeaveService();
