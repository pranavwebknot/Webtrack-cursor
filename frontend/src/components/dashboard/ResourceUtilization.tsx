import React from 'react';
import { Card, Progress, List, Avatar } from 'antd';

interface ResourceData {
  id: number;
  name: string;
  department: string;
  utilization: number;
  avatar?: string;
  projects: string[];
}

interface ResourceUtilizationProps {
  data: ResourceData[];
}

const ResourceUtilization: React.FC<ResourceUtilizationProps> = ({ data }) => {
  const getUtilizationColor = (percentage: number) => {
    if (percentage < 50) return '#52c41a';
    if (percentage < 80) return '#faad14';
    return '#f5222d';
  };

  return (
    <Card title="Resource Utilization">
      <List
        itemLayout="horizontal"
        dataSource={data}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta
              avatar={
                <Avatar src={item.avatar || `https://xsgames.co/randomusers/avatar.php?g=pixel&key=${item.id}`} />
              }
              title={item.name}
              description={`${item.department} • ${item.projects.join(', ')}`}
            />
            <div style={{ width: 180 }}>
              <Progress
                percent={item.utilization}
                strokeColor={getUtilizationColor(item.utilization)}
                size="small"
              />
            </div>
          </List.Item>
        )}
      />
    </Card>
  );
};

export default ResourceUtilization;
