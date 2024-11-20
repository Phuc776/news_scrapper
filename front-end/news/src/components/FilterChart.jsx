import React, { useState } from 'react';
import { DatePicker, Select, Space } from 'antd';

const { RangePicker } = DatePicker;
const { Option } = Select;

const DEFAULT_VALUE = 'Tất cả';

const FilterChart = ({ topics, onFilterChange }) => {
  const [selectedTopic, setSelectedTopic] = useState(DEFAULT_VALUE);
  const [selectedDates, setSelectedDates] = useState([null, null]);

  const handleTopicChange = (value) => {
    setSelectedTopic(value);
    onFilterChange({
      topic: value === DEFAULT_VALUE ? '' : value,
      startDate: selectedDates[0],
      endDate: selectedDates[1],
    });
  };

  const handleDateChange = (dates) => {
    setSelectedDates(dates);
    onFilterChange({
      topic: selectedTopic,
      startDate: dates ? dates[0] : null,
      endDate: dates ? dates[1] : null,
    });
  };

  return (
    <Space style={{ marginBottom: '40px', display: 'flex', justifyContent: 'start' }}>
      <Select
        value={selectedTopic}
        onChange={handleTopicChange}
        placeholder="Chọn topic"
        style={{ width: 200 }}
      >
        {topics.map((topic, index) => (
          <Option key={index} value={topic}>
            {topic}
          </Option>
        ))}
      </Select>

      <RangePicker
        value={selectedDates}
        onChange={handleDateChange}
        format="DD/MM/YYYY"
        style={{ width: 300 }}
      />

    </Space>
  );
};

export default FilterChart;