# HR & Project Management System

A comprehensive HR and project management system built with Django and React, featuring role-based authentication, timesheet management, performance evaluations, and financial reporting.

## Features

- Role-based authentication with multiple user roles (Admin, HR, Sales, Managers, Finance, Employee)
- Timesheet management and approval workflow
- Performance evaluation and appraisal system
- Employee and project allocation tracking
- Leave management system
- Financial reporting and P&L tracking
- Interactive dashboards and analytics

## Tech Stack

### Frontend
- React.js with TypeScript
- Redux Toolkit for state management
- Material UI for components
- Tailwind CSS for styling

### Backend
- Django with Django Rest Framework
- PostgreSQL database
- JWT/OAuth authentication
- Redis for caching

### Infrastructure
- Docker & Kubernetes for containerization
- AWS/Azure/GCP for hosting
- CI/CD with GitHub Actions

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hrm-system
```

2. Backend Setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

3. Frontend Setup:
```bash
cd frontend
npm install
npm start
```

4. Run with Docker:
```bash
docker-compose up --build
```

## Development

### Backend Development
- Follow PEP8 style guide
- Write unit tests using pytest
- Use Django REST framework best practices

### Frontend Development
- Follow ESLint and Prettier configurations
- Write unit tests using Jest and React Testing Library
- Use TypeScript for type safety

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

The application can be deployed using Docker and Kubernetes:

```bash
# Build and push Docker images
docker-compose build
docker-compose push

# Deploy to Kubernetes
kubectl apply -f k8s/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
