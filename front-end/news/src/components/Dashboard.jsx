import React, { useState, useEffect } from 'react';
import styles from './Dashboard.module.scss';
import { Row, Col } from 'antd';
import FilterChart from '../components/FilterChart';
import BarChart from '../components/BarChart';
import PieChart from '../components/PieChart';

const Dashboard = ({ topics, dataTopics, dataCountries, handleFilterDataChange }) => {
  const [filteredDataTopics, setFilteredDataTopics] = useState(dataTopics);

  useEffect(() => {
    setFilteredDataTopics(dataTopics);
  }, [dataTopics]);

  const totalNewsCount = filteredDataTopics.reduce((total, topic) => total + topic.value, 0);

  const handleFilterChange = ({ topic, startDate, endDate }) => {
    console.log(topic, startDate, endDate);
  
    if (startDate && endDate) {
      const formatDate = (date) => {
        if (!date) return null;
        const d = new Date(date);
        return d.toISOString().split('T')[0]; 
      };
  
      const formattedStartDate = formatDate(startDate);
      const formattedEndDate = formatDate(endDate);
      handleFilterDataChange(topic, formattedStartDate, formattedEndDate);
  
      const filtered = dataTopics.filter(item => {
        const isTopicMatch = !topic || item.name === topic;
        const isDateInRange = (!startDate || item.date >= startDate) && 
                              (!endDate || item.date <= endDate);
        return isTopicMatch && isDateInRange;
      });
  
      setFilteredDataTopics(filtered);
    } else {
      setFilteredDataTopics(dataTopics); 
      handleFilterDataChange(topic); 
    }
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
            <PieChart title="Số Lượng Bài Báo Theo Topic" data={filteredDataTopics} tooltipFormatter="{b}: {c} bài báo ({d}%)" />
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
