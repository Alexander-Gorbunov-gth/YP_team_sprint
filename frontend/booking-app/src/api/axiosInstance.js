import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

// Создаем инстанс
const axiosInstance = axios.create();

// Глобальный интерцептор для добавления заголовков
axiosInstance.interceptors.request.use((config) => {
  config.headers['X-Request-Id'] = uuidv4();
  return config;
});

export default axiosInstance;