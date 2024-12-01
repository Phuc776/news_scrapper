import React, { useEffect, useState } from 'react';
import { Layout } from 'antd';
import Sidebar from '../../components/Sidebar/Sidebar';
import AppHeader from '../../components/Header/Header';
import styles from './HomePage.module.scss';
import Dashboard from '../../components/Dashboard';
import Clustering from '../../components/Clustering';

const { Content } = Layout;
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';

const HomePage = () => {

    const [activeItem, setActiveItem] = useState('dashboard');
    const [topics, setTopics] = useState([]);
    const [dataTopics, setdataTopics] = useState([]);
    const [dataCountries, setDataCountries] = useState([]);
    const [clusterData, setClusterData] = useState([]);
    
  
    useEffect(() => {
        fetch(`${API_URL}/articles/news-topics`)
            .then(response => response.json())
            .then(data => {
                setdataTopics(data)
            })
            .catch(error => console.error('Error loading data:', error));
        
        fetch(`${API_URL}/articles/news-countries`)
            .then(response => response.json())
            .then(data => {
                setDataCountries(data)
            })
            .catch(error => console.error('Error loading data:', error));

        fetch(`${API_URL}/articles/topics`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                setTopics([
                    'Tất cả', 
                    ...data.topics
                ])
            })
            .catch(error => console.error('Error loading data:', error));

        fetch(`${API_URL}/clustering/keywords`)
            .then(response => response.json())
            .then(data => {
                setClusterData(data)
            })
            .catch(error => console.error('Error loading data:', error));
    }, []);

    const handleFilterDataChange = (topic, startDate, endDate) => {
        // Tạo URL động cho API countries
        let countriesUrl = `${API_URL}/articles/news-countries?topic=${topic}`;
        if (startDate) countriesUrl += `&start_date=${startDate}`;
        if (endDate) countriesUrl += `&end_date=${endDate}`;
    
        fetch(countriesUrl)
            .then(response => response.json())
            .then(data => {
                setDataCountries(data);
            })
            .catch(error => console.error('Error loading countries data:', error));
    
        // Tạo URL động cho API topic
        let topicUrl = `${API_URL}/articles/news-topics`;
        if (startDate || endDate) {
            topicUrl += '?';
            if (startDate) topicUrl += `start_date=${startDate}`;
            if (endDate) topicUrl += `${startDate ? '&' : ''}end_date=${endDate}`;
        }
    
        fetch(topicUrl)
            .then(response => response.json())
            .then(data => {
                setDataCountries(data);
            })
            .catch(error => console.error('Error loading topic data:', error));
    };

    const handleNavClick = (item) => {
        setActiveItem(item);
      };

    const renderContent = () => {
        switch (activeItem) {
            case 'dashboard':
                return <Dashboard topics={topics} dataCountries={dataCountries} dataTopics={dataTopics} handleFilterDataChange={handleFilterDataChange} />;
            case 'documents':
                return <Clustering data={clusterData} />;
            case 'settings':
                return <div>Settings Content</div>;
            default:
                return <div>Page Not Found</div>;
        }
    }

    return (
        <Layout className={styles.homepage}>
            <Sidebar onNavClick={handleNavClick} activeItem={activeItem} />
            <Layout style={{ marginLeft: 192 }}>
                <AppHeader />
                <Content className={styles.content}>
                    {renderContent()}
                </Content>
            </Layout>
        </Layout>
    );
};

export default HomePage;