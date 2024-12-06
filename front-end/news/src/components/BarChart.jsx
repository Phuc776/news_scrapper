import React from 'react';
import ReactEcharts from 'echarts-for-react';

const BarChart = ({ title, xData, yData, name = 'bài báo' }) => {
  const options = {
    title: {
      text: title,
      left: 'center',
      textStyle: { fontSize: 20, fontWeight: 'bold', color: '#273240' },
    },
    tooltip: { trigger: 'axis', formatter: `{b}: {c} ${name}` },
    xAxis: {
      type: 'category',
      data: xData,
      axisLabel: { rotate: 45 },
      axisLabel: {
        fontSize: 12, // Adjust the font size here
      },
    },
    yAxis: {
      type: 'value', name: name, axisLabel: {
        fontSize: 12, // Adjust the font size here
      },
    },
    series: [
      {
        type: 'bar',
        data: yData,
        barWidth: '50%',
        barCategoryGap: '50%',
        itemStyle: {
          color: function (params) {
            const colors = ['#4689F6', '#6B9FF8', '#90B3FA', '#B5C9FB', '#DBE2FD'];
            return colors[params.dataIndex % colors.length];
          },
        },
      },
    ],
  };

  return <ReactEcharts option={options} style={{ height: '400px' }} />;
};

export default BarChart;