import React, { useEffect, useState } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Tag,
  Modal,
  Form,
  Input,
  Select,
  Rate,
  Tabs,
  message,
} from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';

import performanceService from '../services/performance.service';
import { Performance, PerformanceGoal } from '../types';

const { TextArea } = Input;
const { TabPane } = Tabs;

const PerformancePage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [reviews, setReviews] = useState<Performance[]>([]);
  const [selectedReview, setSelectedReview] = useState<Performance | null>(null);
  const [goals, setGoals] = useState<PerformanceGoal[]>([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  const fetchReviews = async () => {
    try {
      setLoading(true);
      const response = await performanceService.getReviews();
      setReviews(response.results);
    } catch (error) {
      message.error('Failed to fetch performance reviews');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchGoals = async (reviewId: number) => {
    try {
      const response = await performanceService.getGoals(reviewId);
      setGoals(response.results);
    } catch (error) {
      message.error('Failed to fetch goals');
    }
  };

  const handleCreateReview = async (values: any) => {
    try {
      await performanceService.createReview({
        user: values.user,
        reviewer: values.reviewer,
        review_period: values.reviewPeriod,
        review_type: values.reviewType,
        goals: values.goals.map((goal: any) => ({
          description: goal.description,
          category: goal.category,
          weight: goal.weight,
        })),
      });
      message.success('Performance review created successfully');
      setModalVisible(false);
      form.resetFields();
      fetchReviews();
    } catch (error) {
      message.error('Failed to create performance review');
    }
  };

  const handleViewReview = (review: Performance) => {
    setSelectedReview(review);
    fetchGoals(review.id);
  };

  const handleUpdateGoal = async (goalId: number, values: any) => {
    try {
      if (!selectedReview) return;
      await performanceService.updateGoal(selectedReview.id, goalId, {
        rating: values.rating,
        comments: values.comments,
      });
      message.success('Goal updated successfully');
      fetchGoals(selectedReview.id);
    } catch (error) {
      message.error('Failed to update goal');
    }
  };

  const getStatusTag = (status: string) => {
    const colors = {
      DRAFT: 'default',
      SUBMITTED: 'processing',
      REVIEWED: 'warning',
      ACKNOWLEDGED: 'success',
    };
    return <Tag color={colors[status as keyof typeof colors]}>{status}</Tag>;
  };

  const columns = [
    {
      title: 'Employee',
      dataIndex: 'user',
      key: 'user',
    },
    {
      title: 'Reviewer',
      dataIndex: 'reviewer',
      key: 'reviewer',
    },
    {
      title: 'Period',
      dataIndex: 'reviewPeriod',
      key: 'reviewPeriod',
    },
    {
      title: 'Type',
      dataIndex: 'reviewType',
      key: 'reviewType',
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
      render: (_: any, record: Performance) => (
        <Space>
          <Button type="link" onClick={() => handleViewReview(record)}>
            View
          </Button>
          {record.status === 'DRAFT' && (
            <Button type="link" onClick={() => handleSubmitReview(record.id)}>
              Submit
            </Button>
          )}
        </Space>
      ),
    },
  ];

  const handleSubmitReview = async (id: number) => {
    try {
      await performanceService.submitReview(id);
      message.success('Review submitted successfully');
      fetchReviews();
    } catch (error) {
      message.error('Failed to submit review');
    }
  };

  return (
    <div>
      <Card
        title="Performance Reviews"
        extra={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setModalVisible(true)}
          >
            New Review
          </Button>
        }
      >
        <Table
          columns={columns}
          dataSource={reviews}
          rowKey="id"
          loading={loading}
        />
      </Card>

      <Modal
        title="Create Performance Review"
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCreateReview}
        >
          <Form.Item
            name="user"
            label="Employee"
            rules={[{ required: true }]}
          >
            <Select placeholder="Select employee" />
          </Form.Item>

          <Form.Item
            name="reviewer"
            label="Reviewer"
            rules={[{ required: true }]}
          >
            <Select placeholder="Select reviewer" />
          </Form.Item>

          <Form.Item
            name="reviewPeriod"
            label="Review Period"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="reviewType"
            label="Review Type"
            rules={[{ required: true }]}
          >
            <Select>
              <Select.Option value="MID_YEAR">Mid Year</Select.Option>
              <Select.Option value="YEAR_END">Year End</Select.Option>
            </Select>
          </Form.Item>

          <Form.List name="goals">
            {(fields, { add, remove }) => (
              <>
                {fields.map((field, index) => (
                  <Card
                    key={field.key}
                    title={`Goal ${index + 1}`}
                    extra={
                      <Button type="link" danger onClick={() => remove(field.name)}>
                        Remove
                      </Button>
                    }
                    style={{ marginBottom: 16 }}
                  >
                    <Form.Item
                      {...field}
                      name={[field.name, 'description']}
                      label="Description"
                      rules={[{ required: true }]}
                    >
                      <TextArea rows={3} />
                    </Form.Item>

                    <Form.Item
                      {...field}
                      name={[field.name, 'category']}
                      label="Category"
                      rules={[{ required: true }]}
                    >
                      <Input />
                    </Form.Item>

                    <Form.Item
                      {...field}
                      name={[field.name, 'weight']}
                      label="Weight (%)"
                      rules={[{ required: true }]}
                    >
                      <Input type="number" min={0} max={100} />
                    </Form.Item>
                  </Card>
                ))}

                <Form.Item>
                  <Button
                    type="dashed"
                    onClick={() => add()}
                    block
                    icon={<PlusOutlined />}
                  >
                    Add Goal
                  </Button>
                </Form.Item>
              </>
            )}
          </Form.List>

          <Form.Item>
            <Button type="primary" htmlType="submit">
              Create Review
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Review Details"
        visible={!!selectedReview}
        onCancel={() => setSelectedReview(null)}
        width={800}
        footer={null}
      >
        {selectedReview && (
          <Tabs defaultActiveKey="1">
            <TabPane tab="Goals" key="1">
              {goals.map((goal) => (
                <Card key={goal.id} style={{ marginBottom: 16 }}>
                  <h4>{goal.description}</h4>
                  <p>Category: {goal.category}</p>
                  <p>Weight: {goal.weight}%</p>

                  {selectedReview.status !== 'DRAFT' && (
                    <Form
                      initialValues={{
                        rating: goal.rating,
                        comments: goal.comments,
                      }}
                      onFinish={(values) => handleUpdateGoal(goal.id, values)}
                    >
                      <Form.Item name="rating" label="Rating">
                        <Rate />
                      </Form.Item>
                      <Form.Item name="comments" label="Comments">
                        <TextArea rows={3} />
                      </Form.Item>
                      <Form.Item>
                        <Button type="primary" htmlType="submit">
                          Update
                        </Button>
                      </Form.Item>
                    </Form>
                  )}
                </Card>
              ))}
            </TabPane>
            <TabPane tab="Overview" key="2">
              <p>Employee: {selectedReview.user}</p>
              <p>Reviewer: {selectedReview.reviewer}</p>
              <p>Period: {selectedReview.reviewPeriod}</p>
              <p>Type: {selectedReview.reviewType}</p>
              <p>Status: {getStatusTag(selectedReview.status)}</p>
              {selectedReview.overallRating && (
                <p>Overall Rating: <Rate disabled value={selectedReview.overallRating} /></p>
              )}
              {selectedReview.comments && (
                <div>
                  <h4>Comments:</h4>
                  <p>{selectedReview.comments}</p>
                </div>
              )}
            </TabPane>
          </Tabs>
        )}
      </Modal>
    </div>
  );
};

export default PerformancePage;
