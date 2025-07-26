import axios from 'axios';
import { API_BASE } from '../config';

export async function getMyAddresses() {
  try {
    const response = await axios.get(`${API_BASE}/address/my/`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении адресов:', error);
    throw error;
  }
}

export async function createAddress(addressData) {
  try {
    const response = await axios.post(`${API_BASE}/address/`, addressData);
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании адреса:', error);
    throw error;
  }
}

export async function deleteAddress(id) {
  try {
    const response = await axios.delete(`${API_BASE}/address/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при удалении адреса:', error);
    throw error;
  }
}

export async function updateAddress(id, addressData) {
  try {
    const response = await axios.patch(`${API_BASE}/address/${id}/`, addressData);
    return response.data;
  } catch (error) {
    console.error('Ошибка при обновлении адреса:', error);
    throw error;
  }
}