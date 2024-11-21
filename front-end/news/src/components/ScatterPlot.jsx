import React from 'react'
import ReactEcharts from 'echarts-for-react';

const ScatterPlot = ({ title, data }) => {
    const options = {
        title: { text: title, left: 'center', textStyle: { fontSize: 20, fontWeight: 'bold', color: '#273240' } },
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
}

export default ScatterPlot
