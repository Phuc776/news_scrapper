import React, { useState } from 'react';
import styles from './Dashboard.module.scss';
import { Layout, Row, Col, Typography, Spin } from 'antd';
import FilterChart from '../components/FilterChart';
import BarChart from '../components/BarChart';
import LineChart from '../components/LineChart';
import PieChart from '../components/PieChart';
import ScatterPlot from './ScatterPlot';
import StackedBarChart from './StackedBarChart';
import HeatmapChart from './HeatmapChart';

const Dashboard = ({ data, topics }) => {
  const [filters, setFilters] = useState({ topic: '', country: '', month: '' });

  const handleFilterChange = ({ topic, startDate, endDate }) => {
    setFilters({
      ...filters,
      topic,
      country: startDate ? startDate.format('YYYY-MM-DD') : '',
      month: endDate ? endDate.format('YYYY-MM-DD') : '',
    });
  };

  // Filter data based on selected filters
  const filteredData = data.filter((item) => {
    const topicMatch = filters.topic ? item.topic === filters.topic : true;
    const countryMatch = filters.country ? item.country === filters.country : true;
    const monthMatch = filters.month ? new Date(item.published_date).toLocaleString('default', { month: 'long' }) === filters.month : true;
    return topicMatch && countryMatch && monthMatch;
  });


  if (!data || data.length === 0) {
    return (
      <div className={styles.dashboard_loading}>
        <Spin size="large" />
      </div>
    );
  }

  // Pie chart: Number of articles by Topic
  const pieDataTopic = filteredData.reduce((acc, item) => {
    const index = acc.findIndex(topic => topic.name === item.topic);
    if (index >= 0) acc[index].value += 1;
    else acc.push({ name: item.topic, value: 1 });
    return acc;
  }, []);

  // Pie chart: Number of articles by Month of publication
  const pieDataMonth = filteredData.reduce((acc, item) => {
    const month = new Date(item.published_date).toLocaleString('default', { month: 'long' });
    const index = acc.findIndex(m => m.name === month);
    if (index >= 0) acc[index].value += 1;
    else acc.push({ name: month, value: 1 });
    return acc;
  }, []);

  // Bar chart: Number of articles by Country
  const barDataCountry = filteredData.reduce((acc, item) => {
    const index = acc.findIndex(country => country.name === item.country);
    if (index >= 0) acc[index].value += 1;
    else acc.push({ name: item.country, value: 1 });
    return acc;
  }, []);

  const barXData = barDataCountry.map(item => item.name);
  const barYData = barDataCountry.map(item => item.value);

  // Line chart: Average rank by Topic
  const lineData = Object.values(filteredData.reduce((acc, item) => {
    if (!acc[item.topic]) acc[item.topic] = { totalRank: 0, count: 0 };
    acc[item.topic].totalRank += item.rank;
    acc[item.topic].count += 1;
    return acc;
  }, {})).map(({ totalRank, count }) => totalRank / count);

  const lineXData = [...new Set(filteredData.map(item => item.topic))];

  const scatterData = filteredData.map(item => ({
    rank: item.rank,
    published_date: item.published_date,
  }));

  const stackedBarData = filteredData.map(item => ({
    country: item.country,
    topic: item.topic,
  }));

  const heatmapData = filteredData.map(item => ({
    country: item.country,
    published_date: item.published_date,
  }));

  return (
    <div className={styles.dashboard_container}>

      <FilterChart topics={topics} onFilterChange={handleFilterChange} />

      <Row gutter={[16, 16]} justify="center">
        <Col xs={24} md={12}>
          <div className={styles.chart_container}>
            <BarChart title="Số Lượng Bài Báo Theo Country" xData={barXData} yData={barYData} />
          </div>
        </Col>
        <Col xs={24} md={12}>
          <div className={styles.chart_container}>
            <LineChart title="Trung Bình Rank Theo Topic" xData={lineXData} yData={lineData} />
          </div>
        </Col>
        <Col xs={24} md={12}>
          <div className={styles.chart_container}>
            <PieChart title="Số Lượng Bài Báo Theo Topic" data={pieDataTopic} tooltipFormatter="{b}: {c} bài báo ({d}%)" />
          </div>
        </Col>
        <Col xs={24} md={12}>
          <div className={styles.chart_container}>
            <PieChart title="Số Lượng Bài Báo Theo Tháng Xuất Bản" data={pieDataMonth} tooltipFormatter="{b}: {c} bài báo ({d}%)" />
          </div>
        </Col>

        <Col xs={24} md={12}>
          <div className={styles.chart_container}>
            <ScatterPlot title="Scatter Plot: Rank vs Ngày xuất bản" data={scatterData} />
          </div>
        </Col>

        <Col xs={24} md={12}>
          <div className={styles.chart_container}>
            <StackedBarChart title="Stacked Bar Chart: Quốc gia vs Chủ đề" data={stackedBarData} />
          </div>
        </Col>

        <Col xs={24}>
          <div className={styles.chart_container}>
            <HeatmapChart title="Heatmap: Bài báo theo tháng theo quốc gia" data={heatmapData} />
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
