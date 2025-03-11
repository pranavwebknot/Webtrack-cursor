import React from 'react';
import { Card, Statistic } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

interface MetricsCardProps {
  title: string;
  value: number | string;
  prefix?: React.ReactNode;
  suffix?: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

const MetricsCard: React.FC<MetricsCardProps> = ({
  title,
  value,
  prefix,
  suffix,
  trend,
}) => {
  return (
    <Card>
      <Statistic
        title={title}
        value={value}
        prefix={prefix}
        suffix={suffix}
        valueStyle={{ color: '#3f8600' }}
      />
      {trend && (
        <div style={{ marginTop: 8 }}>
          <span style={{ color: trend.isPositive ? '#3f8600' : '#cf1322' }}>
            {trend.isPositive ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            {Math.abs(trend.value)}%
          </span>
          <span style={{ marginLeft: 8, color: 'rgba(0, 0, 0, 0.45)' }}>
            vs last period
          </span>
        </div>
      )}
    </Card>
  );
};

export default MetricsCard;
