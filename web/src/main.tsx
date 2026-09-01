import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { App } from './App';
import './styles/global.css';

createRoot(document.getElementById('root')!).render(<StrictMode><ConfigProvider theme={{ token: { colorPrimary: '#1677ff', borderRadius: 6, fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' } }}><BrowserRouter><App /></BrowserRouter></ConfigProvider></StrictMode>);
