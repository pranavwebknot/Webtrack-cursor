import React from 'react';
import { Card } from 'antd';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface ProjectHealthData {
  name: string;
  onTrack: number;
  atRisk: number;
  delayed: number;
}

interface ProjectHealthChartProps {
  data: ProjectHealthData[];
}

const ProjectHealthChart: React.FC<ProjectHealthChartProps> = ({ data }) => {
  return (
    <Card title="Project Health Overview">
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <BarChart
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="onTrack" name="On Track" fill="#52c41a" stackId="a" />
            <Bar dataKey="atRisk" name="At Risk" fill="#faad14" stackId="a" />
            <Bar dataKey="delayed" name="Delayed" fill="#f5222d" stackId="a" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

export default ProjectHealthChart;
