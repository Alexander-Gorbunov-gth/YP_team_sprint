

import axios from 'axios';
import { API_AUTH_BASE } from '../config';


export const registerUser = async (formData) => {
  console.log('Registering user with data:', formData);
  const response = await axios.post(
    `${API_AUTH_BASE}/register/`,
    JSON.stringify(formData),
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data;
};

export const loginUser = async (formData) => {
  console.log('Logging in with data:', formData);
  const response = await axios.post(
    `${API_AUTH_BASE}/login/`,
    JSON.stringify(formData),
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data;
};