import api from './api';
import { Performance, PerformanceGoal, Skill } from '../types';
import { mockPerformanceData } from './mockData';

interface PerformanceCreateData {
  user: number;
  reviewer: number;
  review_period: string;
  review_type: 'MID_YEAR' | 'YEAR_END';
  goals: {
    description: string;
    category: string;
    weight: number;
  }[];
}

interface PerformanceUpdateData {
  overall_rating?: number;
  status?: 'DRAFT' | 'SUBMITTED' | 'REVIEWED' | 'ACKNOWLEDGED';
  comments?: string;
  goals?: {
    id?: number;
    description?: string;
    category?: string;
    weight?: number;
    rating?: number;
    comments?: string;
  }[];
}

class PerformanceService {
  // Performance Reviews
  async getReviews(params?: {
    user?: number;
    reviewer?: number;
    status?: string;
    review_type?: string;
  }) {
    try {
      const response = await api.get<{ results: Performance[] }>('/api/reviews/', { params });
      return response.data;
    } catch (error) {
      console.warn('Using mock data for performance reviews:', error);
      return { results: mockPerformanceData.reviews };
    }
  }

  async getReview(id: number) {
    try {
      const response = await api.get<Performance>(`/api/reviews/${id}/`);
      return response.data;
    } catch (error) {
      console.warn('Using mock data for performance review:', error);
      return mockPerformanceData.reviews.find(r => r.id === id);
    }
  }

  async createReview(data: PerformanceCreateData) {
    try {
      const response = await api.post<Performance>('/api/reviews/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating performance review:', error);
      throw error;
    }
  }

  async updateReview(id: number, data: PerformanceUpdateData) {
    try {
      const response = await api.patch<Performance>(`/api/reviews/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating performance review:', error);
      throw error;
    }
  }

  async deleteReview(id: number) {
    try {
      await api.delete(`/api/reviews/${id}/`);
    } catch (error) {
      console.error('Error deleting performance review:', error);
      throw error;
    }
  }

  async submitReview(id: number) {
    try {
      const response = await api.post<Performance>(`/api/reviews/${id}/submit/`);
      return response.data;
    } catch (error) {
      console.error('Error submitting performance review:', error);
      throw error;
    }
  }

  async acknowledgeReview(id: number) {
    try {
      const response = await api.post<Performance>(`/api/reviews/${id}/acknowledge/`);
      return response.data;
    } catch (error) {
      console.error('Error acknowledging performance review:', error);
      throw error;
    }
  }

  // Goals
  async getGoals(reviewId: number) {
    try {
      const response = await api.get<{ results: PerformanceGoal[] }>(`/api/reviews/${reviewId}/goals/`);
      return response.data;
    } catch (error) {
      console.warn('Using mock data for performance goals:', error);
      return { results: mockPerformanceData.goals.filter(g => g.performanceId === reviewId) };
    }
  }

  async updateGoal(reviewId: number, goalId: number, data: {
    rating: number;
    comments: string;
  }) {
    try {
      const response = await api.patch<PerformanceGoal>(`/api/reviews/${reviewId}/goals/${goalId}/`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating performance goal:', error);
      throw error;
    }
  }

  // Skills
  async getSkills() {
    try {
      const response = await api.get<{ results: Skill[] }>('/api/skills/');
      return response.data;
    } catch (error) {
      console.error('Error fetching skills:', error);
      throw error;
    }
  }

  async createSkill(data: { name: string; category: string }) {
    try {
      const response = await api.post<Skill>('/api/skills/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating skill:', error);
      throw error;
    }
  }

  async updateSkill(id: number, data: { name?: string; category?: string }) {
    try {
      const response = await api.patch<Skill>(`/api/skills/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error('Error updating skill:', error);
      throw error;
    }
  }

  async deleteSkill(id: number) {
    try {
      await api.delete(`/api/skills/${id}/`);
    } catch (error) {
      console.error('Error deleting skill:', error);
      throw error;
    }
  }

  // Analytics
  async getPerformanceAnalytics(params?: {
    department?: string;
    period?: string;
  }) {
    try {
      const response = await api.get('/api/reviews/analytics/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching performance analytics:', error);
      throw error;
    }
  }

  async getSkillMatrix(params?: {
    department?: string;
  }) {
    try {
      const response = await api.get('/api/skills/matrix/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching skill matrix:', error);
      throw error;
    }
  }
}

export default new PerformanceService();
