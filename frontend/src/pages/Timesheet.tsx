import React, { useEffect, useState } from 'react';
import {
  Card,
  Table,
  Form,
  Input,
  DatePicker,
  InputNumber,
  Button,
  Select,
  Space,
  message,
  Tag,
} from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';

import timesheetService from '../services/timesheet.service';
import { Timesheet } from '../types';

const { RangePicker } = DatePicker;
const { TextArea } = Input;

const TimesheetPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [timesheets, setTimesheets] = useState<Timesheet[]>([]);
  const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs]>([
    dayjs().startOf('month'),
    dayjs().endOf('month'),
  ]);

  const fetchTimesheets = async () => {
    try {
      setLoading(true);
      const response = await timesheetService.getTimesheets({
        start_date: dateRange[0].format('YYYY-MM-DD'),
        end_date: dateRange[1].format('YYYY-MM-DD'),
      });
      setTimesheets(response.results);
    } catch (error) {
      message.error('Failed to fetch timesheets');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimesheets();
  }, [dateRange]);

  const handleSubmit = async (values: any) => {
    try {
      await timesheetService.createTimesheet({
        project: values.project,
        date: values.date.format('YYYY-MM-DD'),
        hours: values.hours,
        description: values.description,
      });
      message.success('Timesheet entry added successfully');
      form.resetFields();
      fetchTimesheets();
    } catch (error) {
      message.error('Failed to submit timesheet entry');
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
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (date: string) => dayjs(date).format('YYYY-MM-DD'),
    },
    {
      title: 'Project',
      dataIndex: 'project',
      key: 'project',
    },
    {
      title: 'Hours',
      dataIndex: 'hours',
      key: 'hours',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
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
      render: (_: any, record: Timesheet) => (
        <Space>
          {record.status === 'PENDING' && (
            <>
              <Button
                type="link"
                onClick={() => handleEdit(record)}
              >
                Edit
              </Button>
              <Button
                type="link"
                danger
                onClick={() => handleDelete(record.id)}
              >
                Delete
              </Button>
            </>
          )}
        </Space>
      ),
    },
  ];

  const handleEdit = (record: Timesheet) => {
    // Implement edit functionality
  };

  const handleDelete = async (id: number) => {
    try {
      await timesheetService.deleteTimesheet(id);
      message.success('Timesheet entry deleted successfully');
      fetchTimesheets();
    } catch (error) {
      message.error('Failed to delete timesheet entry');
    }
  };

  return (
    <div>
      <Card title="Add Timesheet Entry" style={{ marginBottom: 16 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="project"
            label="Project"
            rules={[{ required: true, message: 'Please select a project' }]}
          >
            <Select
              placeholder="Select project"
              options={projects.map(p => ({ label: p.name, value: p.id }))}
            />
          </Form.Item>

          <Form.Item
            name="date"
            label="Date"
            rules={[{ required: true, message: 'Please select a date' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item
            name="hours"
            label="Hours"
            rules={[
              { required: true, message: 'Please enter hours' },
              { type: 'number', min: 0, max: 24, message: 'Hours must be between 0 and 24' },
            ]}
          >
            <InputNumber style={{ width: '100%' }} step={0.5} />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter a description' }]}
          >
            <TextArea rows={4} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
              Add Entry
            </Button>
          </Form.Item>
        </Form>
      </Card>

      <Card title="Timesheet History">
        <div style={{ marginBottom: 16 }}>
          <Space>
            <RangePicker
              value={dateRange}
              onChange={(dates) => dates && setDateRange(dates)}
            />
            <Button icon={<SearchOutlined />} onClick={fetchTimesheets}>
              Search
            </Button>
          </Space>
        </div>

        <Table
          columns={columns}
          dataSource={timesheets}
          rowKey="id"
          loading={loading}
        />
      </Card>
    </div>
  );
};

export default TimesheetPage;
