import api from './api';
import { Timesheet } from '../types';
import { mockTimesheetData } from './mockData';

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
    try {
      const response = await api.get<{ results: Timesheet[] }>('/api/timesheets/', { params });
      return response.data;
    } catch (error) {
      console.warn('Using mock data for timesheets:', error);
      return { results: mockTimesheetData.timesheets };
    }
  }

  async getTimesheet(id: number) {
    try {
      const response = await api.get<Timesheet>(`/api/timesheets/${id}/`);
      return response.data;
    } catch (error) {
      console.warn('Using mock data for timesheet:', error);
      return mockTimesheetData.timesheets.find(t => t.id === id);
    }
  }

  async createTimesheet(data: TimesheetCreateData) {
    try {
      const response = await api.post<Timesheet>('/api/timesheets/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating timesheet:', error);
      throw error;
    }
  }

  async updateTimesheet(id: number, data: TimesheetUpdateData) {
    try {
      const response = await api.patch<Timesheet>(`/api/timesheets/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating timesheet:', error);
      throw error;
    }
  }

  async deleteTimesheet(id: number) {
    try {
      await api.delete(`/api/timesheets/${id}/`);
    } catch (error) {
      console.error('Error deleting timesheet:', error);
      throw error;
    }
  }

  async approveTimesheet(id: number) {
    try {
      const response = await api.post<Timesheet>(`/api/timesheets/${id}/approve/`);
      return response.data;
    } catch (error) {
      console.error('Error approving timesheet:', error);
      throw error;
    }
  }

  async rejectTimesheet(id: number, reason: string) {
    try {
      const response = await api.post<Timesheet>(`/api/timesheets/${id}/reject/`, { reason });
      return response.data;
    } catch (error) {
      console.error('Error rejecting timesheet:', error);
      throw error;
    }
  }

  async getProjects() {
    try {
      const response = await api.get('/api/projects/');
      return response.data;
    } catch (error) {
      console.warn('Using mock data for projects:', error);
      return { results: mockTimesheetData.projects };
    }
  }

  async getTimesheetSummary(params?: {
    start_date?: string;
    end_date?: string;
    project?: number;
    user?: number;
  }) {
    try {
      const response = await api.get('/api/timesheets/summary/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching timesheet summary:', error);
      throw error;
    }
  }
}

export default new TimesheetService();
