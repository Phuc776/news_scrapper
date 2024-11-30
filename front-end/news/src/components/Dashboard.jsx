import React, { useState } from 'react';
import styles from './Dashboard.module.scss';
import { Row, Col } from 'antd';
import FilterChart from '../components/FilterChart';
import BarChart from '../components/BarChart';
import PieChart from '../components/PieChart';

const Dashboard = ({ topics, dataTopics, dataCountries, handleFilterDataChange }) => {
  const totalNewsCount = dataTopics.reduce((total, topic) => total + topic.value, 0);

  const handleFilterChange = ({ topic, startDate, endDate }) => {
    console.log(topic, startDate, endDate)
    if (startDate && endDate){
      const formatDate = (date) => {
          if (!date) return null; // Trả về null nếu không có giá trị
          const d = new Date(date);
          return d.toISOString().split('T')[0]; // Định dạng YYYY-MM-DD
      };

      const formattedStartDate = formatDate(startDate);
      const formattedEndDate = formatDate(endDate);
      handleFilterDataChange(topic, formattedStartDate, formattedEndDate);
    }
        
    else handleFilterDataChange(topic);
  };

  const barXData = dataCountries.map(item => item.name);
  const barYData = dataCountries.map(item => item.value);


  return (
    <div className={styles.dashboard_container} style={{'marginTop': '48px'}}>
      <Row gutter={[16, 16]} justify="center">
        <Col xs={24} md={12} style={{'position': 'relative'}}>
          <div className={styles.chart_container}>
            <BarChart title="Số Lượng Bài Báo Theo Country" xData={barXData} yData={barYData} />
          </div>
          <FilterChart topics={topics} onFilterChange={handleFilterChange} />
        </Col>
        <Col xs={24} md={12} style={{'position': 'relative'}}>
          <div className={styles.chart_container}>
            <PieChart title="Số Lượng Bài Báo Theo Topic" data={dataTopics} tooltipFormatter="{b}: {c} bài báo ({d}%)" />
          </div>
          <div style={{
            'position': 'absolute', 
            'bottom': '24px', 
            'right': '32px',
            'display': 'flex',
            'alignItems': 'center',
            'gap': '8px',
            'fontSize': '16px',
          }}>
              <span style={{
                'display': 'inline-block',
                'backgroundColor': '#4689F6',
                'width': '16px',
                'height': '16px',
              }}></span>
              <p>Tổng số bài báo: {totalNewsCount}</p>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
