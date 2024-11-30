import React, { useState } from 'react';
import { DatePicker, Select, Space } from 'antd';

const { RangePicker } = DatePicker;
const { Option } = Select;

const DEFAULT_VALUE = 'Tất cả';

const FilterChart = ({ topics, onFilterChange }) => {
  const [selectedTopic, setSelectedTopic] = useState(DEFAULT_VALUE);
  const [selectedDates, setSelectedDates] = useState(["", ""]);

  const handleTopicChange = (value) => {
    setSelectedTopic(value);
    onFilterChange({
      topic: value === DEFAULT_VALUE ? '' : value,
      startDate: selectedDates ? selectedDates[0] : "",
      endDate: selectedDates ? selectedDates[1] : "",
    });
  };

  const handleDateChange = (dates) => {
    setSelectedDates(dates);
    onFilterChange({
      topic: selectedTopic === DEFAULT_VALUE ? '' : selectedTopic,
      startDate: dates ? dates[0] : "",
      endDate: dates ? dates[1] : "",
    });
  };

  return (
    <>
      <div style={{
        'position': 'absolute', 
        'top': '12px', 
        'right': '12px',
        'display': 'flex',
        'alignItems': 'center',
        'gap': '8px',
        'fontSize': '16px',
      }}>
        <Space style={{ marginBottom: '40px', display: 'flex', justifyContent: 'start' }}>
          <Select
            value={selectedTopic}
            onChange={handleTopicChange}
            placeholder="Chọn topic"
            style={{ width: 100, border: '1px solid #d9d9d9', borderRadius: '6px' }}
          >
            {topics.map((topic, index) => (
              <Option key={index} value={topic}>
                {topic}
              </Option>
            ))}
          </Select>
        </Space>
      </div>
      <div style={{
        'position': 'absolute',
        'top': '-70px',
        'right': '-120px',
      }}>
        <RangePicker
          value={selectedDates}
          onChange={handleDateChange}
          format="DD/MM/YYYY"
          style={{ width: 400, height: 40 }}
        />
      </div>
    </>
  );
};

export default FilterChart;