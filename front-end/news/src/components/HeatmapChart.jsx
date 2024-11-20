import React from 'react';
import ReactEcharts from 'echarts-for-react';

const HeatmapChart = ({ title, data }) => {
  const countries = Array.from(new Set(data.map(item => item.country)));
  const months = Array.from({ length: 12 }, (_, i) => new Date(0, i).toLocaleString('default', { month: 'long' }));
  const heatmapData = [];

  months.forEach((month, monthIdx) => {
    countries.forEach((country, countryIdx) => {
      const count = data.filter(
        item =>
          new Date(item.published_date).toLocaleString('default', { month: 'long' }) === month &&
          item.country === country
      ).length;
      heatmapData.push([countryIdx, monthIdx, count]);
    });
  });

  const options = {
    title: { text: title, left: 'center' },
    tooltip: { position: 'top' },
    xAxis: { type: 'category', data: countries, splitArea: { show: true } },
    yAxis: { type: 'category', data: months, splitArea: { show: true } },
    visualMap: {
      min: 0,
      max: Math.max(...heatmapData.map(d => d[2])),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '15%',
      inRange: {
        color: ['#DBF0F8', '#93CAE1', '#B0D9F1'],
      },
    },
    series: [
      {
        type: 'heatmap',
        data: heatmapData,
        label: { show: true },
      },
    ],
  };

  return <ReactEcharts option={options} style={{ height: '400px' }} />;
};

export default HeatmapChart;
