import React, { useEffect, useState } from 'react';
import Dashboard from '../components/Dashboard';

function App() {
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

  return <Dashboard data={data} topics={topics} />;
}

export default App;
