export interface User {
  id: number;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  role: string;
  department: string;
  position: string;
  phoneNumber: string;
  dateOfBirth: string;
  dateOfJoining: string;
  isActive: boolean;
}

export interface Timesheet {
  id: number;
  user: number;
  project: number;
  date: string;
  hours: number;
  description: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  submittedAt: string;
  approvedBy?: number;
  approvedAt?: string;
  rejectionReason?: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  client: string;
  startDate: string;
  endDate: string;
  status: 'NOT_STARTED' | 'IN_PROGRESS' | 'ON_HOLD' | 'COMPLETED' | 'CANCELLED';
  budget: number;
  actualCost: number;
}

export interface Client {
  id: number;
  name: string;
  company: string;
  email: string;
  phone: string;
  address: string;
}

export interface Performance {
  id: number;
  user: number;
  reviewer: number;
  reviewPeriod: string;
  reviewType: 'MID_YEAR' | 'YEAR_END';
  overallRating?: number;
  status: 'DRAFT' | 'SUBMITTED' | 'REVIEWED' | 'ACKNOWLEDGED';
  submittedAt?: string;
  reviewedAt?: string;
  acknowledgedAt?: string;
  comments?: string;
}

export interface PerformanceGoal {
  id: number;
  performanceId: number;
  description: string;
  category: string;
  weight: number;
  rating?: number;
  comments?: string;
}

export interface Skill {
  id: number;
  name: string;
  category: string;
}

export interface Leave {
  id: number;
  user: number;
  leaveType: string;
  startDate: string;
  endDate: string;
  daysRequested: number;
  reason: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  approvedBy?: number;
  approvedAt?: string;
  rejectionReason?: string;
}

export interface Allocation {
  id: number;
  user: User;
  project: Project;
  start_date: string;
  end_date: string;
  allocation_percentage: number;
  role: string;
  billing_rate: number;
}

export interface ProjectFinancials {
  id: number;
  name: string;
  budget: number;
  actualCost: number;
  variance: number;
  profitMargin: number;
}

export interface DashboardMetrics {
  revenue: number;
  revenueTrend: number;
  activeProjects: number;
  projectsTrend: number;
  teamMembers: number;
  avgUtilization: number;
  utilizationTrend: number;
}

export interface Task {
  id: number;
  projectId: number;
  title: string;
  description: string;
  assignedTo: number;
  status: 'TODO' | 'IN_PROGRESS' | 'REVIEW' | 'DONE';
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  startDate: string;
  dueDate: string;
}

export interface Notification {
  id: number;
  user: number;
  title: string;
  message: string;
  type: 'INFO' | 'SUCCESS' | 'WARNING' | 'ERROR';
  isRead: boolean;
  createdAt: string;
  link?: string;
}
