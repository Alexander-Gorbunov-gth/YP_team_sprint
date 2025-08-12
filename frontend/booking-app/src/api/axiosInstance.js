import axios from 'axios';
import { API_AUTH_BASE } from '../config';
import { v4 as uuidv4 } from 'uuid';
import { AppError } from "./AppError";
import { showErrorToast } from '../ui/showErrorToast'; // <-- добавили

const axiosInstance = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

axiosInstance.interceptors.request.use((config) => {
  config.headers = config.headers || {};
  config.headers['X-Request-Id'] = uuidv4();
  return config;
});

axiosInstance.interceptors.response.use(
  (res) => res,
  (error) => {
    const status = error?.response?.status ?? 0;
    const data = error?.response?.data;

    let appError;

    if (data?.error) {
      const { code, message, details } = data.error;
      appError = new AppError({ code, message, details, status });
    } else if (data?.detail) {
      let messageText;
      if (Array.isArray(data.detail)) {
        messageText = data.detail
          .map((d) => {
            if (typeof d === 'string') return d;
            const loc = Array.isArray(d.loc) ? d.loc.join('.') : d.loc;
            const msg = d.msg || d.message || '';
            return loc ? `${loc}: ${msg}` : msg || 'Validation error';
          })
          .join('; ');
      } else {
        messageText = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
      }
      appError = new AppError({ code: 'DETAIL', message: messageText, status });
    } else if (data?.message) {
      appError = new AppError({ message: data.message, status });
    } else if (!error.response) {
      appError = new AppError({ message: 'Сетевая ошибка: сервер недоступен', status: 0 });
    } else {
      appError = new AppError({ message: error.message || 'Неизвестная ошибка', status });
    }

    // 📢 Показываем тост с ошибкой в любом случае
    showErrorToast(appError);

    return Promise.reject(appError);
  }
);

export default axiosInstance;