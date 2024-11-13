import React from 'react';
import ReactEcharts from 'echarts-for-react';

const StackedBarChart = ({ title, data }) => {
  const countries = Array.from(new Set(data.map(item => item.country)));
  const topics = Array.from(new Set(data.map(item => item.topic)));

  const seriesData = topics.map(topic => ({
    name: topic,
    type: 'bar',
    stack: 'total',
    data: countries.map(country => data.filter(item => item.country === country && item.topic === topic).length),
  }));

  const options = {
    title: { 
        text: title, 
        left: 'center', 
        top: '10px',
        textStyle: { fontSize: 18, fontWeight: 'bold' } 
    },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: {
        bottom: '10px',
        left: 'center',
        orient: 'horizontal',
    },
    xAxis: { type: 'category', data: countries },
    yAxis: { type: 'value', name: 'Số lượng bài báo' },
    series: seriesData,
  };

  return <ReactEcharts option={options} style={{ height: '400px' }} />;
};

export default StackedBarChart;
