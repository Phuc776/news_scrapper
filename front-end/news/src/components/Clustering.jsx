import React, { useEffect, useState } from 'react';
import PieChart from './PieChart';
import BarChart from './BarChart';
import ClusteringChart from './ClusteringChart';
import { DatePicker, Select, Space } from 'antd';
import styles from './Dashboard.module.scss';
import { Row, Col } from 'antd';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';

const Clustering = ({ data, handleFilterDateClustering }) => {
    const [dates, setDates] = useState([]);

    useEffect(() => {
        const fetchDates = async () => {
            const response = await fetch(`${API_URL}/clustering/distinct-dates`);
            const data = await response.json();
            setDates(data);
        }
        fetchDates();
    }, [])

    const handleFilter = (date) => {
        handleFilterDateClustering(date);
    }

    console.log(dates);

    const keywordWeightData = data.map(cluster => {
        const keywords = cluster.keywords.split(',');
        const weights = cluster.weights.split(',');
        return keywords.map((keyword, index) => ({
            keyword,
            weight: parseFloat(weights[index]),
            cluster: cluster.cluster_name,
        }));
    }).flat();

    const keywordClusterData = data.map(cluster => {
        const keywords = cluster.keywords.split(',');
        return keywords.map(keyword => ({
            keyword,
            cluster: cluster.cluster_name,
        }));
    }).flat();

    const keywordWeightXData = keywordWeightData.map(item => item.keyword);
    const keywordWeightYData = keywordWeightData.map(item => item.weight);
    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    return (
        <div>
            <Select
                // value={selectedTopic}
                onChange={handleFilter}
                placeholder="Seletec date"
                style={{ width: 400, border: '1px solid #d9d9d9', borderRadius: '6px' }}
            >
                {dates.map(date => (
                    <Select.Option key={date} value={date}>{formatDate(date)}</Select.Option>
                ))}
            </Select>
            {/* <h1>Date: {formatDate(data[0].created_at)}</h1> */}
            <Col style={{ 'position': 'relative' }}>
                <div className={styles.chart_container}>
                    <BarChart
                        title="Keyword / Weight"
                        xData={keywordWeightXData}
                        yData={keywordWeightYData}
                        name='weight'
                    />
                </div>
            </Col>
            <Col style={{ 'position': 'relative', 'marginTop': '32px' }}>
                <div className={styles.chart_container}>
                    <ClusteringChart data={data} />
                </div>
            </Col>
        </div >
    );
};

export default Clustering;