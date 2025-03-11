import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { ConfigProvider } from 'antd';
import { store } from './store';
import theme from './theme';
import MainLayout from './layouts/MainLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Timesheet from './pages/Timesheet';
import Leave from './pages/Leave';
import Performance from './pages/Performance';
import ProtectedRoute from './components/ProtectedRoute';

// Placeholder components for other pages
const Projects = () => <div>Projects Page</div>;
const Team = () => <div>Team Page</div>;
const Reports = () => <div>Reports Page</div>;

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: theme.colors.primary,
            colorSuccess: theme.colors.success,
            colorWarning: theme.colors.warning,
            colorError: theme.colors.error,
            colorInfo: theme.colors.info,
            colorTextBase: theme.colors.text.primary,
            colorBgBase: theme.colors.background.light,
            borderRadius: parseInt(theme.borderRadius.md),
            fontFamily: theme.typography.fontFamily,
          },
        }}
      >
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
              <Route index element={<Dashboard />} />
              <Route path="timesheet" element={<Timesheet />} />
              <Route path="leave" element={<Leave />} />
              <Route path="performance" element={<Performance />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ConfigProvider>
    </Provider>
  );
};

export default App;
