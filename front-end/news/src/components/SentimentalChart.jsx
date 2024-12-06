import React from 'react';
import ReactECharts from 'echarts-for-react';
import CorrelationHeatmap from './CorrelationChart';
import styles from './Dashboard.module.scss';
import { Row, Col } from 'antd';

const SentimentalChart = ({ data, correlationData }) => {
    // Prepare data for the chart
    const topics = data.map((item) => `${item.topic} ${"\n"} (${item.article_count} news)`);
    const avgSentimentScores = data.map((item) => item.avg_sentiment_score);

    const options = {
        title: {
            text: 'Topic Sentiment Scores',
            left: 'center',
            textStyle: {
                fontSize: 20, // Adjust the font size here
            },
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow', // Display a shadow for bar charts
            },
        },
        xAxis: {
            type: 'category',
            data: topics,
            axisLabel: {
                rotate: 45, // Rotate labels for better visibility
                margin: 20,
                fontSize: 12, // Adjust the font size here
            },
        },
        yAxis: {
            type: 'value',
            name: 'Avg Sentiment Score',
            axisLabel: {
                fontSize: 12, // Adjust the font size here
            },
        },
        series: [
            {
                name: 'Avg Sentiment Score',
                type: 'bar',
                barWidth: '60%',
                barCategoryGap: '100%',
                data: avgSentimentScores,
                itemStyle: {
                    color: '#4689F6', // Custom bar color
                },

            },
        ],
    };

    return <div>
        <Col style={{ 'position': 'relative' }}>
            <div className={styles.chart_container}>
                <ReactECharts option={options} style={{ height: 400, width: '100%' }} />;
            </div>
        </Col>
        <Col style={{ 'position': 'relative', 'marginTop': '32px' }}>
            <div className={styles.chart_container}>
                <CorrelationHeatmap correlationData={correlationData} />
            </div>
        </Col>
    </div>
};

export default SentimentalChart;
