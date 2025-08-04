import { API_BASE } from "../config";
import axiosInstance from "./axiosInstance";
import { getAuthHeaders } from "./authHeaders";

export async function getMySubscriptions() {
  const response = await axiosInstance.get(`${API_BASE}/subscribe/my/`, {
    headers: getAuthHeaders()
  });
  return response.data;
}

export async function deleteSubscription(hostId) {
  const response = await axiosInstance.delete(`${API_BASE}/subscribe/`, {
    headers: getAuthHeaders(),
    data: {
      host_id: hostId
    }
  });
  return response.data;
}   

export async function createSubscription(subscriptionData) {
  const response = await axiosInstance.post(
    `${API_BASE}/subscribe/`, 
    subscriptionData,
    {
      headers: getAuthHeaders(),
    }
  );
  return response.data;
}
