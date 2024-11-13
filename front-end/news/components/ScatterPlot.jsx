import React from 'react'
import ReactEcharts from 'echarts-for-react';

const ScatterPlot = ({ title, data }) => {
    const options = {
        title: { text: title, left: 'center', textStyle: { fontSize: 20, fontWeight: 'bold' } },
        tooltip: { trigger: 'axis', formatter: '{b}: Rank {c}' },
        xAxis: {
          type: 'category',
          data: data.map(item => item.published_date),
          axisLabel: { rotate: 45 },
        },
        yAxis: { type: 'value', name: 'Rank' },
        series: [
          {
            type: 'scatter',
            data: data.map(item => [item.published_date, item.rank]),
            symbolSize: 10,
          },
        ],
    };

    return <ReactEcharts option={options} style={{ height: '400px' }} />;
}

export default ScatterPlot
