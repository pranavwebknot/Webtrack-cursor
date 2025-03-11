import React, { useEffect, useState } from 'react';
import {
  Card,
  Table,
  Form,
  Input,
  DatePicker,
  Button,
  Select,
  Space,
  message,
  Tag,
  Row,
  Col,
  Statistic,
} from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';

import leaveService from '../services/leave.service';
import { Leave } from '../types';

const { RangePicker } = DatePicker;
const { TextArea } = Input;

const LeavePage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [leaveRequests, setLeaveRequests] = useState<Leave[]>([]);
  const [leaveBalance, setLeaveBalance] = useState<any>(null);
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().startOf('month'),
    dayjs().endOf('month'),
  ]);

  const fetchLeaveData = async () => {
    try {
      setLoading(true);
      const [requestsResponse, balanceResponse] = await Promise.all([
        leaveService.getLeaveRequests({
          start_date: dateRange[0].format('YYYY-MM-DD'),
          end_date: dateRange[1].format('YYYY-MM-DD'),
        }),
        leaveService.getLeaveBalance(),
      ]);
      setLeaveRequests(requestsResponse.results);
      setLeaveBalance(balanceResponse);
    } catch (error) {
      message.error('Failed to fetch leave data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaveData();
  }, [dateRange]);

  const handleSubmit = async (values: any) => {
    try {
      await leaveService.createLeaveRequest({
        leave_type: values.leaveType,
        start_date: values.dateRange[0].format('YYYY-MM-DD'),
        end_date: values.dateRange[1].format('YYYY-MM-DD'),
        reason: values.reason,
      });
      message.success('Leave request submitted successfully');
      form.resetFields();
      fetchLeaveData();
    } catch (error) {
      message.error('Failed to submit leave request');
    }
  };

  const getStatusTag = (status: string) => {
    const colors = {
      PENDING: 'gold',
      APPROVED: 'green',
      REJECTED: 'red',
    };
    return <Tag color={colors[status as keyof typeof colors]}>{status}</Tag>;
  };

  const columns = [
    {
      title: 'Leave Type',
      dataIndex: 'leaveType',
      key: 'leaveType',
    },
    {
      title: 'Start Date',
      dataIndex: 'startDate',
      key: 'startDate',
      render: (date: string) => dayjs(date).format('YYYY-MM-DD'),
    },
    {
      title: 'End Date',
      dataIndex: 'endDate',
      key: 'endDate',
      render: (date: string) => dayjs(date).format('YYYY-MM-DD'),
    },
    {
      title: 'Days',
      dataIndex: 'daysRequested',
      key: 'daysRequested',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => getStatusTag(status),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Leave) => (
        <Space>
          {record.status === 'PENDING' && (
            <Button
              type="link"
              danger
              onClick={() => handleCancel(record.id)}
            >
              Cancel
            </Button>
          )}
        </Space>
      ),
    },
  ];

  const handleCancel = async (id: number) => {
    try {
      await leaveService.deleteLeaveRequest(id);
      message.success('Leave request cancelled successfully');
      fetchLeaveData();
    } catch (error) {
      message.error('Failed to cancel leave request');
    }
  };

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Annual Leave"
              value={leaveBalance?.annual || 0}
              suffix="days"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Sick Leave"
              value={leaveBalance?.sick || 0}
              suffix="days"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Personal Leave"
              value={leaveBalance?.personal || 0}
              suffix="days"
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Other Leave"
              value={leaveBalance?.other || 0}
              suffix="days"
            />
          </Card>
        </Col>
      </Row>

      <Card title="Request Leave" style={{ marginBottom: 16 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="leaveType"
            label="Leave Type"
            rules={[{ required: true, message: 'Please select leave type' }]}
          >
            <Select>
              <Select.Option value="ANNUAL">Annual Leave</Select.Option>
              <Select.Option value="SICK">Sick Leave</Select.Option>
              <Select.Option value="PERSONAL">Personal Leave</Select.Option>
              <Select.Option value="OTHER">Other Leave</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="dateRange"
            label="Date Range"
            rules={[{ required: true, message: 'Please select date range' }]}
          >
            <RangePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="reason"
            label="Reason"
            rules={[{ required: true, message: 'Please enter reason' }]}
          >
            <TextArea rows={4} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
              Submit Request
            </Button>
          </Form.Item>
        </Form>
      </Card>

      <Card title="Leave History">
        <div style={{ marginBottom: 16 }}>
          <Space>
            <RangePicker
              value={dateRange}
              onChange={(dates) => dates && setDateRange(dates)}
            />
            <Button icon={<SearchOutlined />} onClick={fetchLeaveData}>
              Search
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={leaveRequests}
          rowKey="id"
          loading={loading}
        />
      </Card>
    </div>
  );
};

export default LeavePage;
