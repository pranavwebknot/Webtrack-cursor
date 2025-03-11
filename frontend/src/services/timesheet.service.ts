import api from './api';
import { Timesheet } from '../types';

interface TimesheetCreateData {
  project: number;
  date: string;
  hours: number;
  description: string;
}

interface TimesheetUpdateData extends TimesheetCreateData {
  status?: 'PENDING' | 'APPROVED' | 'REJECTED';
}

class TimesheetService {
  async getTimesheets(params?: {
    start_date?: string;
    end_date?: string;
    project?: number;
    user?: number;
    status?: string;
  }) {
    const response = await api.get<{ results: Timesheet[] }>('/timesheets/', { params });
    return response.data;
  }

  async getTimesheet(id: number) {
    const response = await api.get<Timesheet>(`/timesheets/${id}/`);
    return response.data;
  }

  async createTimesheet(data: TimesheetCreateData) {
    const response = await api.post<Timesheet>('/timesheets/', data);
    return response.data;
  }

  async updateTimesheet(id: number, data: TimesheetUpdateData) {
    const response = await api.patch<Timesheet>(`/timesheets/${id}/`, data);
    return response.data;
  }

  async deleteTimesheet(id: number) {
    await api.delete(`/timesheets/${id}/`);
  }

  async approveTimesheet(id: number) {
    const response = await api.post<Timesheet>(`/timesheets/${id}/approve/`);
    return response.data;
  }

  async rejectTimesheet(id: number, reason: string) {
    const response = await api.post<Timesheet>(`/timesheets/${id}/reject/`, { reason });
    return response.data;
  }

  async getTimesheetSummary(params?: {
    start_date?: string;
    end_date?: string;
    project?: number;
    user?: number;
  }) {
    const response = await api.get('/timesheets/summary/', { params });
    return response.data;
  }
}

export default new TimesheetService();
