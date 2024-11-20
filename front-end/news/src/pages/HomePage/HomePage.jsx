import React, { useEffect, useState } from 'react';
import { Layout } from 'antd';
import Sidebar from '../../components/Sidebar/Sidebar';
import AppHeader from '../../components/Header/Header';
import styles from './HomePage.module.scss';
import Dashboard from '../../components/Dashboard';

const { Content } = Layout;

const HomePage = () => {

    const [activeItem, setActiveItem] = useState('dashboard');
    const [data, setData] = useState([]);
    const [topics, setTopics] = useState([]);
  
    useEffect(() => {
      fetch('/data.json')
        .then(response => response.json())
        .then(data => {
          setData(data)
          setTopics(['Tất cả', ...new Set(data.map(item => item.topic))]);
        })
        .catch(error => console.error('Error loading data:', error));
    }, []);

    const renderContent = () => {
        switch (activeItem) {
            case 'dashboard':
                return <Dashboard data={data} topics={topics} />;
            case 'documents':
                return <div>Documents Content</div>;
            case 'settings':
                return <div>Settings Content</div>;
            default:
                return <div>Page Not Found</div>;
        }
    }

    const handleNavClick = (item) => {
        setActiveItem(item);
      };

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