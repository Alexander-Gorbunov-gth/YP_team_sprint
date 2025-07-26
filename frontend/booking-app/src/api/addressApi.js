

import axios from 'axios';
import { API_BASE } from '../config';

export async function getMyAddresses() {
    return [
        {
            id: "uuid-a1",
            country: "Россия",
            city: "Москва",
            street: "Тверская",
            house: "10",
            flat: null
        },
        {
            id: "uuid-a2",
            country: "Россия",
            city: "Санкт-Петербург",
            street: "Невский проспект",
            house: "25",
            flat: "3"
        }
    ]
  try {
    const response = await axios.get(`${API_BASE}/addresses/my`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении адресов:', error);
    throw error;
  }
}