

import { API_BASE } from "../config";
import axios from "axios";

export async function getMySubscriptions(userId) {
    return [
  {
    host_id: "uuid-o1",
    author: {
      id: "uuid-o1",
      name: "Иван Иванов",
      username: "ivan123"
    }
  },
  {
    host_id: "uuid-o2",
    author: {
      id: "uuid-o2",
      name: "Мария Смирнова",
      username: "masha_s"
    }
  }
];
  const response = await axios.get(`${API_BASE}/subscriptions`, {
    params: { user_id: userId }
  });
  return response.data;
}

export async function deleteSubscription(hostId) {
  const response = await axios.delete(`${API_BASE}/subscriptions`, {
    data: {
      host_id: hostId
    }
  });
  return response.data;
}   

export async function createSubscription(subscriptionData) {
  const response = await axios.post(`${API_BASE}/subscriptions`, subscriptionData);
  return response.data;
}