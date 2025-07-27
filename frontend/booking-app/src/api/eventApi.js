import axios from 'axios';
import { API_BASE } from '../config';

export async function getEvents() {
  const res = await axios.get(`${API_BASE}/events/`);
  return res.data;
}


export async function getEventById(id) {
  const res = await axios.get(`${API_BASE}/events/${id}`);
  return res.data;
}



export async function getMyEvents() {
  const res = await axios.get(`${API_BASE}/events/my/`);
  return res.data;
}

export async function createEvent(eventData) {
  console.log("Создание события с данными:", eventData);
  try {
    const res = await axios.post(`${API_BASE}/events`, eventData);
    return res.data;
  } catch (error) {
    console.error("Ошибка при создании события:", error);
    throw error;
  }
}

export async function updateEvent(id, data) {
  console.log(data)
  const res = await axios.patch(`${API_BASE}/events/${id}`, data);
  return res.data;
}