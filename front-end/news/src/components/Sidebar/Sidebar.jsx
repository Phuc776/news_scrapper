import React from 'react';
import { Layout } from 'antd';
import styles from './Sidebar.module.scss';
import { LuLayoutDashboard } from "react-icons/lu";
import { GrCluster } from "react-icons/gr";

const { Sider } = Layout;

const Sidebar = ({ onNavClick, activeItem }) => {
  return (
    <Sider className={styles.sidebar}>
      <ul className={styles.nav_list}>
        <li
          className={`${styles.nav_item} ${activeItem === 'dashboard' ? styles.active : ''}`}
          onClick={() => onNavClick('dashboard')}
        >
          <LuLayoutDashboard size={20} className={styles.icon}/>
          <span className={styles.nav_text}>Dashboard</span>
        </li>
        <li
          className={`${styles.nav_item} ${activeItem === 'documents' ? styles.active : ''}`}
          onClick={() => onNavClick('documents')}
        >
          <GrCluster size={20} className={styles.icon} />
          <span className={styles.nav_text}>Clustering</span>
        </li>
        <li
          className={`${styles.nav_item} ${activeItem === 'settings' ? styles.active : ''}`}
          onClick={() => onNavClick('settings')}
        >
          <LuLayoutDashboard size={20} className={styles.icon}/>
          <span className={styles.nav_text}>Settings</span>
        </li>
      </ul>
    </Sider>
  );
};

export default Sidebar;
