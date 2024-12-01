import React from 'react';
import ReactECharts from 'echarts-for-react';

const ClusteringChart = ({ data }) => {
    // Tạo dữ liệu cho biểu đồ phân tán (scatter chart)
    const scatterData = data.map((cluster, index) => {
        const keywords = cluster.keywords.split(',');
        const weights = cluster.weights.split(',');

        return keywords.map((keyword, i) => ({
            name: keyword,
            value: [index, parseFloat(weights[i])], // index là số thứ tự cụm, weight là giá trị Y
            label: {
                show: true,
                position: 'top',
                formatter: keyword, // Hiển thị từ khóa
            }
        }));
    }).flat();

    // Các cụm trên trục X (các cluster)
    const clusterNames = data.map(cluster => cluster.cluster_name);

    // Cấu hình biểu đồ ECharts
    const option = {
        title: {
            text: 'Clustering Keywords with Weights',
            left: 'center',
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                return `${params.data.name}<br/>Weight: ${params.data.value[1]}`;
            }
        },
        xAxis: {
            type: 'category',
            name: 'Clusters',
            data: clusterNames,
            axisLabel: {
                interval: 0, // Đảm bảo tất cả các nhãn cụm được hiển thị
                rotate: 45, // Xoay nhãn nếu cần
            }
        },
        yAxis: {
            type: 'value',
            name: 'Weight',
        },
        series: [
            {
                type: 'scatter',
                data: scatterData,
                symbolSize: 10, // Kích thước điểm
                itemStyle: {
                    color: '#4689F6', // Màu của các điểm
                },
                label: {
                    show: true,
                    formatter: '{b}', // Hiển thị từ khóa
                    position: 'top',
                    fontSize: 10,
                }
            }
        ]
    };

    return <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />;
};

export default ClusteringChart;