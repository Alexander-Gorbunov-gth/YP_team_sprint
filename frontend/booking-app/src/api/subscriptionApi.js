

import { API_BASE } from "../config";
import axios from "axios";

export async function getMySubscriptions(userId) {
    return [
  {
    host_id: "00000000-0000-0000-0000-000000000001",
    author: {
      id: "00000000-0000-0000-0000-000000000001",
      name: "Иван Иванов",
      username: "ivan123"
    }
  },
  {
    host_id: "00000000-0000-0000-0000-000000000002",
    author: {
      id: "00000000-0000-0000-0000-000000000002",
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