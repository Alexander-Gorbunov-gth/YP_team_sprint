import axios from 'axios';
import { API_AUTH_BASE } from '../config';

const postJson = async (url, data) => {
  const response = await axios.post(url, JSON.stringify(data), {
    headers: {
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};

export const registerUser = async (formData) => {
  console.log('Registering user with data:', formData);
  return postJson(`${API_AUTH_BASE}/auth/register/`, formData);
};

export const loginUser = async (formData) => {
  console.log('Logging in with data:', formData);
  return postJson(`${API_AUTH_BASE}/auth/login/`, formData);
};