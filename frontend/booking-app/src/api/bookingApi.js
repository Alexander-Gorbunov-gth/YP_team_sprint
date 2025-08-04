import axios from 'axios';
import { API_BASE } from '../config';
import { getAuthHeaders } from "./authHeaders";
import axiosInstance from "./axiosInstance";


export async function createReservation(payload) {
  const res = await axiosInstance.post(`${API_BASE}/reservation/`, payload, {
    headers: getAuthHeaders()
  });
  return res.data;
}

export async function getBookingsByUser() {
  const res = await axiosInstance.get(`${API_BASE}/reservation/`, {
    headers: getAuthHeaders()
  });
  return res.data;
}


export async function getBookingById(id) {
  const res = await axiosInstance.get(`${API_BASE}/reservation/${id}`, {
    headers: getAuthHeaders()
  });
  return res.data;
}

export async function updateBookingStatus(id, newStatus) {
  console.log("Updating booking status:", id, newStatus);
  const res = await axiosInstance.patch(`${API_BASE}/reservation/${id}`, { status: newStatus }, {
    headers: getAuthHeaders()
  });
  return res.data;
}
