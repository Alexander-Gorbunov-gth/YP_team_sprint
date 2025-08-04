import axios from 'axios';
import { API_AUTH_BASE } from '../config';
import { v4 as uuidv4 } from 'uuid';

const axiosInstance = axios.create({
  baseURL: API_AUTH_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерсептор для запроса — добавляем X-Request-Id
axiosInstance.interceptors.request.use((config) => {
  config.headers['X-Request-Id'] = uuidv4();
  return config;
});

// Интерсептор для ответа — обработка ошибок
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;

    if (status === 401) {
      window.location.href = '/login'; // редирект на логин
    }

    if (status >= 400 && status < 500) {
      console.warn('Client error:', error.response);
      window.location.href = '/error';
    }

    if (status >= 500) {
      console.error('Server error:', error.response);
      alert('Произошла ошибка сервера. Попробуйте позже.');
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;