import React, { useState } from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useNavigate, useLocation } from 'react-router-dom';
import authService from '../services/auth.service';
import WebknotLogo from '../components/WebknotLogo';

interface LocationState {
  from: {
    pathname: string;
  };
}

const Login: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as LocationState)?.from?.pathname || '/';

  const onFinish = async (values: { username: string; password: string }) => {
    try {
      setLoading(true);
      await authService.login(values);
      message.success('Login successful');
      navigate(from, { replace: true });
    } catch (error) {
      message.error('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
      padding: '20px',
    }}>
      <Card
        style={{
          width: '100%',
          maxWidth: 400,
          boxShadow: '0 4px 24px rgba(0, 0, 0, 0.1)',
          borderRadius: '12px',
        }}
        bodyStyle={{
          padding: '32px',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ marginBottom: 16 }}>
            <WebknotLogo width={64} height={64} />
          </div>
          <h1 style={{
            fontSize: '24px',
            margin: 0,
            color: '#6B46C1',
            fontWeight: 700,
            letterSpacing: '2px',
          }}>
            WEBKNOT
          </h1>
          <h2 style={{
            fontSize: '28px',
            margin: '16px 0 0',
            color: '#2C3E50',
            fontWeight: 600,
            letterSpacing: '-0.5px',
          }}>
            WebTrack
          </h2>
          <p style={{
            margin: '8px 0 0',
            color: '#6C757D',
            fontSize: '15px',
            fontWeight: 500,
          }}>
            Employee Management System
          </p>
        </div>
        <Form
          name="login"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          layout="vertical"
          size="large"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Please input your username!' }]}
          >
            <Input
              prefix={<UserOutlined style={{ color: '#6C757D' }} />}
              placeholder="Username"
              style={{ borderRadius: '8px' }}
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Please input your password!' }]}
          >
            <Input.Password
              prefix={<LockOutlined style={{ color: '#6C757D' }} />}
              placeholder="Password"
              style={{ borderRadius: '8px' }}
            />
          </Form.Item>

          <Form.Item style={{ marginBottom: 12 }}>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              block
              style={{
                height: '44px',
                borderRadius: '8px',
                fontSize: '16px',
                fontWeight: 500,
                background: '#6B46C1',
                border: 'none',
              }}
            >
              Sign In
            </Button>
          </Form.Item>
        </Form>
        <div style={{ textAlign: 'center', marginTop: 24 }}>
          <a
            href="https://webknot.in"
            target="_blank"
            rel="noopener noreferrer"
            style={{
              color: '#6C757D',
              fontSize: '14px',
              textDecoration: 'none',
              transition: 'color 0.2s',
            }}
            onMouseOver={(e) => e.currentTarget.style.color = '#6B46C1'}
            onMouseOut={(e) => e.currentTarget.style.color = '#6C757D'}
          >
            © {new Date().getFullYear()} Webknot Technologies
          </a>
        </div>
      </Card>
    </div>
  );
};

export default Login;
