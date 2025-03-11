import api from './api';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  department: string;
  position: string;
  phone_number: string;
  date_of_birth: string;
  date_of_joining: string;
}

export interface ChangePasswordData {
  old_password: string;
  new_password: string;
}

export interface ResetPasswordData {
  email: string;
}

export interface ResetPasswordConfirmData {
  uid: string;
  token: string;
  new_password: string;
}

class AuthService {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>('/api/token/', credentials);
    if (response.data.access) {
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
  }

  async logout(): Promise<void> {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
  }

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/users/me/');
    return response.data;
  }

  async refreshToken(): Promise<AuthResponse> {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) throw new Error('No refresh token available');

    const response = await api.post<AuthResponse>('/api/token/refresh/', {
      refresh: refreshToken,
    });

    if (response.data.access) {
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }

    return response.data;
  }

  async changePassword(data: ChangePasswordData): Promise<void> {
    await api.post('/users/change_password/', data);
  }

  async resetPassword(data: ResetPasswordData): Promise<void> {
    await api.post('/users/reset_password/', data);
  }

  async resetPasswordConfirm(data: ResetPasswordConfirmData): Promise<void> {
    await api.post('/users/reset_password_confirm/', data);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
}

export default new AuthService();
