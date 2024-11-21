import React from 'react';
import ReactEcharts from 'echarts-for-react';

// Component để render biểu đồ Pie
const PieChart = ({ title, data, tooltipFormatter }) => {
  const options = {
    title: {
      text: title,
      left: 'center',
      textStyle: { fontSize: 20, fontWeight: 'bold', color: '#273240' },
    },
    tooltip: { trigger: 'item', formatter: tooltipFormatter },
    series: [
      {
        type: 'pie',
        data: data,
        radius: '60%',
        label: { formatter: '{b}: {c}' },
        itemStyle: {
          color: function (params) {
            const colors = ['#4689F6', '#6B9FF8', '#90B3FA', '#B5C9FB'];
            return colors[params.dataIndex % colors.length];
          },
        },
      },
    ],
  };

  return <ReactEcharts option={options} style={{ height: '400px' }} />;
};

export default PieChart;