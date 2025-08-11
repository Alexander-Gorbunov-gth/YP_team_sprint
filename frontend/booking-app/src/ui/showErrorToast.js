import toast from 'react-hot-toast';

export function showErrorToast(error) {
  let msg = 'Что-то пошло не так. Попробуйте ещё раз.';

  // Если это ответ от axios
  if (error?.response?.data) {
    const data = error.response.data;

    if (data?.error?.message) {
      // Наш стандартный формат от бэкенда
      msg = data.error.message;
    } else if (typeof data === 'string') {
      // Иногда бэк может вернуть строку
      msg = data;
    }
  } else if (error?.message) {
    // Если это AppError или другая ошибка JS
    msg = error.message;
  }

  toast.error(msg, {
    style: {
      borderRadius: '10px',
      background: '#222',
      color: '#fff',
      padding: '12px 16px',
      fontSize: '14px',
      maxWidth: '400px',
      whiteSpace: 'pre-line', // чтобы переносились строки
    },
    duration: 5000,
  });
}