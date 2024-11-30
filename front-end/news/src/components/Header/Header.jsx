import React from 'react';
import { Layout, Input, Avatar, Image } from 'antd';
import avatar from '../../assets/avatar.png';
import logo from '../../assets/logo.png';
import styles from './Header.module.scss';
import { IconBellRinging, IconLogout } from '@tabler/icons-react';

const { Header } = Layout;

const AppHeader = () => {

    return (
        <Header className={styles.header_container}>
            <div className={styles.logo}>
                <Image
                    preview={false}
                    src={logo}
                />
            </div>

            <h1>News Analytics</h1>

            <div className={styles.user_actions}>
                <IconBellRinging size={24}/>
                <Avatar
                    size="large"
                    src={avatar}
                    alt="User Avatar"
                />
                <p className={styles.name}>Vitamin DataMining</p>
                <IconLogout size={24}/>
            </div>
        </Header>
    );
};

export default AppHeader;
