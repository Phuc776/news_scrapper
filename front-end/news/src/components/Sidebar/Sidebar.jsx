import React from 'react';
import { Layout } from 'antd';
import { IconFile, IconHome, IconSettings } from '@tabler/icons-react';
import styles from './Sidebar.module.scss';

const { Sider } = Layout;

const Sidebar = ({ onNavClick, activeItem }) => {
  return (
    <Sider className={styles.sidebar}>
      <ul className={styles.nav_list}>
        <li
          className={`${styles.nav_item} ${activeItem === 'dashboard' ? styles.active : ''}`}
          onClick={() => onNavClick('dashboard')}
        >
          <IconHome size={20} className={styles.icon}/>
          <span className={styles.nav_text}>Dashboard</span>
        </li>
        <li
          className={`${styles.nav_item} ${activeItem === 'documents' ? styles.active : ''}`}
          onClick={() => onNavClick('documents')}
        >
          <IconFile size={20} className={styles.icon} />
          <span className={styles.nav_text}>Documents</span>
        </li>
        <li
          className={`${styles.nav_item} ${activeItem === 'settings' ? styles.active : ''}`}
          onClick={() => onNavClick('settings')}
        >
          <IconSettings size={20} className={styles.icon}/>
          <span className={styles.nav_text}>Settings</span>
        </li>
      </ul>
    </Sider>
  );
};

export default Sidebar;
