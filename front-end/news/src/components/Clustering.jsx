import React from 'react';
import PieChart from './PieChart';
import BarChart from './BarChart';
import ClusteringChart from './ClusteringChart';

const Clustering = ({data}) => {
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
        {/* Biểu đồ Keyword / Weight */}
        <h1>Date: {formatDate(data[0].created_at)}</h1>
        <BarChart
            title="Keyword / Weight"
            xData={keywordWeightXData}
            yData={keywordWeightYData}
            name='weight'
        />
        <ClusteringChart data={data} />
    </div>
    );
};

export default Clustering;