

import { API_BASE } from "../config";
import axios from "axios";

export async function getMySubscriptions() {
  const response = await axios.get(`${API_BASE}/subscribe/my/`);
  return response.data;
}

export async function deleteSubscription(hostId) {
  const response = await axios.delete(`${API_BASE}/subscribe/`, {
    data: {
      host_id: hostId
    }
  });
  return response.data;
}   

export async function createSubscription(subscriptionData) {
  const response = await axios.post(`${API_BASE}/subscribe/`, subscriptionData);
  return response.data;
}
