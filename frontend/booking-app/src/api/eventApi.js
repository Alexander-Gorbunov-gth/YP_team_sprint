import axios from 'axios';
import { API_BASE } from '../config';
import { getAuthHeaders } from "./authHeaders";
import axiosInstance from "./axiosInstance";

export async function getEvents({ offset = 0, limit = 10 }) {
  const res = await axiosInstance.get(`${API_BASE}/events/`, {
    headers: getAuthHeaders(),
    params: { offset, limit },
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
  try {
    const res = await axiosInstance.post(`${API_BASE}/events/`, eventData, {
      headers: getAuthHeaders(),
    });
    return res.data;
  } catch (error) {
    console.error("Ошибка при создании события:", error);
    throw error;
  }
}

export async function createEventReserv(event_id, seats) {
  const res = await axiosInstance.post(
    `${API_BASE}/events/${event_id}/reserve/`,
    { event_id, seats },
    { headers: getAuthHeaders() }
  );
  return res.data;
}

export async function updateEvent(id, data) {
  const res = await axiosInstance.patch(`${API_BASE}/events/${id}`, data, {
    headers: getAuthHeaders(),
  });
  return res.data;
}

export async function deleteEvent(id) {
  const res = await axiosInstance.delete(`${API_BASE}/events/${id}`, {
    headers: getAuthHeaders(),
  });
  return res.data;
}

export async function getNearbyEvents({ addressId, radiusKm = 5 }) {
  const body = { address: addressId, radius: Number(radiusKm) };
  console.log(body);
  const { data } = await axiosInstance.post(
    `${API_BASE}/events/nearby/`,
    body,
    { headers: getAuthHeaders() }
  );
  return data; // list[EventResponseSchema]
}