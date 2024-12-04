import React from 'react';
import ReactECharts from 'echarts-for-react';

const CorrelationHeatmap = ({ correlationData }) => {
    const correlationMatrix = correlationData.correlation_data.correlation_matrix;

    // Prepare data for heatmap
    const variables = Object.keys(correlationMatrix);
    const heatmapData = [];

    variables.forEach((rowKey, rowIndex) => {
        variables.forEach((colKey, colIndex) => {
            heatmapData.push([rowIndex, colIndex, correlationMatrix[rowKey][colKey]]);
        });
    });

    const options = {
        title: {
            text: 'Correlation Heatmap',
            left: 'center',
            textStyle: {
                fontSize: 20, // Adjust the font size here
            },
        },
        tooltip: {
            position: 'top',
            formatter: (params) => {
                const [row, col, value] = params.value;
                return `${variables[row]} & ${variables[col]}: ${value.toFixed(2)}`;
            },
        },
        xAxis: {
            type: 'category',
            data: variables,
            splitArea: { show: true },
            axisLabel: {
                fontSize: 14, // Adjust the font size here
            },
        },
        yAxis: {
            type: 'category',
            data: variables,
            splitArea: { show: true },
            axisLabel: {
                fontSize: 14, // Adjust the font size here
            },
        },
        visualMap: {
            min: -1,
            max: 1,
            calculable: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            inRange: {
                color: ['#2c7bb6', '#abd9e9', '#ffffbf', '#fdae61', '#d7191c'],
            },
        },
        series: [
            {
                name: 'Correlation',
                type: 'heatmap',
                data: heatmapData,
                label: {
                    show: true,
                    formatter: ({ value }) => value[2].toFixed(2),
                    fontSize: 16, // Adjust the font size here
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)',
                    },
                },
            },
        ],
    };

    return <ReactECharts option={options} style={{ height: 800, width: '100%' }} />;
};

export default CorrelationHeatmap;