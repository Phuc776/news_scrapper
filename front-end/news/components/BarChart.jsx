import React from 'react';
import ReactEcharts from 'echarts-for-react';

const BarChart = ({ title, xData, yData }) => {
    const options = {
      title: {
        text: title,
        left: 'center',
        textStyle: { fontSize: 20, fontWeight: 'bold' },
      },
      tooltip: { trigger: 'axis', formatter: '{b}: {c} bài báo' },
      xAxis: {
        type: 'category',
        data: xData,
        axisLabel: { rotate: 45 },
      },
      yAxis: { type: 'value', name: 'Số lượng' },
      series: [
        {
          type: 'bar',
          data: yData,
          barWidth: '60%',
          barCategoryGap: '50%',
        },
      ],
    };
  
    return <ReactEcharts option={options} style={{ height: '400px' }} />;
  };

export default BarChart;