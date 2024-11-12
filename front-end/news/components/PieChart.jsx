import React from 'react';
import ReactEcharts from 'echarts-for-react';

// Component để render biểu đồ Pie
const PieChart = ({ title, data, tooltipFormatter }) => {
  const options = {
    title: {
      text: title,
      left: 'center',
      textStyle: { fontSize: 20, fontWeight: 'bold' },
    },
    tooltip: { trigger: 'item', formatter: tooltipFormatter },
    series: [
      {
        type: 'pie',
        data: data,
        radius: '60%',
        label: { formatter: '{b}: {c}' },
      },
    ],
  };

  return <ReactEcharts option={options} style={{ height: '400px' }} />;
};

export default PieChart;