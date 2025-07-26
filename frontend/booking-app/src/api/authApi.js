

import axios from 'axios';
import { API_AUTH_BASE } from '../config';


export const registerUser = async (formData) => {
  const response = await axios.post(`${API_AUTH_BASE}/register`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const loginUser = async (formData) => {
  const response = await axios.post(`${API_AUTH_BASE}/login`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};