import React from 'react';
import ReactEcharts from 'echarts-for-react';

const LineChart = ({ title, xData, yData }) => {
  const options = {
    title: {
      text: title,
      left: 'center',
      textStyle: { fontSize: 20, fontWeight: 'bold', color: '#273240' },
    },
    tooltip: { trigger: 'axis', formatter: '{b}: Rank trung bình {c}' },
    xAxis: {
      type: 'category',
      data: xData,
      axisLabel: { fontSize: 14, rotate: 0, margin: 20 },
      axisLine: { lineStyle: { color: '#B0B0B0', width: 1 } },
    },
    yAxis: { type: 'value', name: 'Rank trung bình' },
    series: [
      {
        type: 'line',
        data: yData,
        smooth: true,
        itemStyle: {
          color: '#4689F6',
        },
      },
    ],
  };

  return <ReactEcharts option={options} style={{ height: '400px' }} />;
};

export default LineChart;