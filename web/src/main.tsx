import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ConfigProvider, theme } from 'antd';
import { App } from './App';
import './styles/global.css';

createRoot(document.getElementById('root')!).render(<StrictMode><ConfigProvider theme={{ algorithm: theme.darkAlgorithm, token: { colorPrimary: '#d8b06b', colorBgBase: '#081012', colorBgContainer: '#101d20', colorBorder: '#29413e', borderRadius: 4, fontFamily: 'Manrope, sans-serif' } }}><BrowserRouter><App /></BrowserRouter></ConfigProvider></StrictMode>);
