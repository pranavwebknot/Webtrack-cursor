import api from './api';
import { Performance, PerformanceGoal, Skill } from '../types';

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
    const response = await api.get<{ results: Performance[] }>('/reviews/', { params });
    return response.data;
  }

  async getReview(id: number) {
    const response = await api.get<Performance>(`/reviews/${id}/`);
    return response.data;
  }

  async createReview(data: PerformanceCreateData) {
    const response = await api.post<Performance>('/reviews/', data);
    return response.data;
  }

  async updateReview(id: number, data: PerformanceUpdateData) {
    const response = await api.patch<Performance>(`/reviews/${id}/`, data);
    return response.data;
  }

  async deleteReview(id: number) {
    await api.delete(`/reviews/${id}/`);
  }

  async submitReview(id: number) {
    const response = await api.post<Performance>(`/reviews/${id}/submit/`);
    return response.data;
  }

  async acknowledgeReview(id: number) {
    const response = await api.post<Performance>(`/reviews/${id}/acknowledge/`);
    return response.data;
  }

  // Goals
  async getGoals(reviewId: number) {
    const response = await api.get<{ results: PerformanceGoal[] }>(`/reviews/${reviewId}/goals/`);
    return response.data;
  }

  async updateGoal(reviewId: number, goalId: number, data: {
    rating: number;
    comments: string;
  }) {
    const response = await api.patch<PerformanceGoal>(`/reviews/${reviewId}/goals/${goalId}/`, data);
    return response.data;
  }

  // Skills
  async getSkills() {
    const response = await api.get<{ results: Skill[] }>('/skills/');
    return response.data;
  }

  async createSkill(data: { name: string; category: string }) {
    const response = await api.post<Skill>('/skills/', data);
    return response.data;
  }

  async updateSkill(id: number, data: { name?: string; category?: string }) {
    const response = await api.patch<Skill>(`/skills/${id}/`, data);
    return response.data;
  }

  async deleteSkill(id: number) {
    await api.delete(`/skills/${id}/`);
  }

  // Analytics
  async getPerformanceAnalytics(params?: {
    department?: string;
    period?: string;
  }) {
    const response = await api.get('/reviews/analytics/', { params });
    return response.data;
  }

  async getSkillMatrix(params?: {
    department?: string;
  }) {
    const response = await api.get('/skills/matrix/', { params });
    return response.data;
  }
}

export default new PerformanceService();
