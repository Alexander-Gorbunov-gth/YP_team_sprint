import axios from 'axios';
import { API_BASE } from '../config';
import { getAuthHeaders } from "./authHeaders";
import axiosInstance from "./axiosInstance";

export async function getEvents() {
  const res = await axiosInstance.get(`${API_BASE}/events/`, {
    headers: getAuthHeaders(),
  });
  return res.data;
}


export async function getEventById(id) {
  const res = await axiosInstance.get(`${API_BASE}/events/${id}`, {
    headers: getAuthHeaders(),
  });
  return res.data;
}



export async function getMyEvents() {
  const res = await axiosInstance.get(`${API_BASE}/events/my/`, {
    headers: getAuthHeaders(),
  });
  return res.data;
}

export async function createEvent(eventData) {
  console.log("Создание события с данными:", eventData);
  try {
    const res = await axiosInstance.post(`${API_BASE}/events`, eventData, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error) {
    console.error("Ошибка при создании события:", error);
    throw error;
  }
}

export async function updateEvent(id, data) {
  console.log(data)
  const res = await axiosInstance.patch(`${API_BASE}/events/${id}`, data, {
    headers: getAuthHeaders(),
  });
  return res.data;
}