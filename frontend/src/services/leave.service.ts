import api from './api';
import { Leave } from '../types';

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
    const response = await api.get<{ results: Leave[] }>('/leave-requests/', { params });
    return response.data;
  }

  async getLeaveRequest(id: number) {
    const response = await api.get<Leave>(`/leave-requests/${id}/`);
    return response.data;
  }

  async createLeaveRequest(data: LeaveRequestCreateData) {
    const response = await api.post<Leave>('/leave-requests/', data);
    return response.data;
  }

  async updateLeaveRequest(id: number, data: LeaveRequestUpdateData) {
    const response = await api.patch<Leave>(`/leave-requests/${id}/`, data);
    return response.data;
  }

  async deleteLeaveRequest(id: number) {
    await api.delete(`/leave-requests/${id}/`);
  }

  async approveLeaveRequest(id: number) {
    const response = await api.post<Leave>(`/leave-requests/${id}/approve/`);
    return response.data;
  }

  async rejectLeaveRequest(id: number, reason: string) {
    const response = await api.post<Leave>(`/leave-requests/${id}/reject/`, { reason });
    return response.data;
  }

  // Leave Balances
  async getLeaveBalance(userId?: number) {
    const response = await api.get('/leave-balances/', {
      params: userId ? { user: userId } : undefined,
    });
    return response.data;
  }

  // Leave Types
  async getLeaveTypes() {
    const response = await api.get('/leave-types/');
    return response.data;
  }

  // Leave Policies
  async getLeavePolicies() {
    const response = await api.get('/leave-policies/');
    return response.data;
  }

  // Analytics
  async getLeaveAnalytics(params?: {
    department?: string;
    year?: number;
  }) {
    const response = await api.get('/leave-requests/analytics/', { params });
    return response.data;
  }

  async getTeamCalendar(params?: {
    department?: string;
    month?: string;
  }) {
    const response = await api.get('/leave-requests/calendar/', { params });
    return response.data;
  }
}

export default new LeaveService();
