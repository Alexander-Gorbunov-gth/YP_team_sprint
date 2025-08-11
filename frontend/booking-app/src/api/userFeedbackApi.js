// src/api/userFeedbackApi.js
import { API_BASE } from "../config";
import axiosInstance from "./axiosInstance";
import { getAuthHeaders } from "./authHeaders";

const FEEDBACK_API = API_BASE + "/user-feedback/";

export async function createUserFeedback(data) {
  const res = await axiosInstance.post(
    FEEDBACK_API,
    data,
    { headers: getAuthHeaders() }
  );
  return res.data;
}

export async function deleteUserFeedback(reviewUserId) {
  const res = await axiosInstance.delete(`${FEEDBACK_API}/${String(reviewUserId)}`, {
    headers: getAuthHeaders(),
  });
  return res.data;
}