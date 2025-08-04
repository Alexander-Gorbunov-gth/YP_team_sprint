import axios from 'axios';
import { API_BASE } from '../config';
import { getAuthHeaders } from "./authHeaders";
import axiosInstance from "./axiosInstance";

export async function getMyAddresses() {
  try {
    const response = await axiosInstance.get(`${API_BASE}/address/my/`, {
      headers: getAuthHeaders()
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении адресов:', error);
    throw error;
  }
}

export async function createAddress(addressData) {

  try {
    const response = await axiosInstance.post(`${API_BASE}/address/`, addressData, {
      headers: getAuthHeaders()
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании адреса:', error);
    throw error;
  }
}

export async function deleteAddress(id) {
  try {
    const response = await axiosInstance.delete(`${API_BASE}/address/${id}/`, {
      headers: getAuthHeaders()
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка при удалении адреса:', error);
    throw error;
  }
}

export async function updateAddress(id, addressData) {
  try {
    const response = await axiosInstance.patch(`${API_BASE}/address/${id}/`, addressData, {
      headers: getAuthHeaders()
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка при обновлении адреса:', error);
    throw error;
  }
}