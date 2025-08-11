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


// --- Event feedback API ---
const EVENT_FEEDBACK_API = API_BASE + "/event-feedback/";

/**
 * Получить агрегированные оценки по мероприятию и мою оценку
 * Ожидаемый ответ бэка:
 * { event_id, my: "positive"|"negative"|null, positive: number, negative: number }
 */
export async function getEventFeedback(eventId) {
  const { data } = await axiosInstance.get(
    `${EVENT_FEEDBACK_API}${String(eventId)}`,
    { headers: getAuthHeaders() }
  );
  return {
    event_id: data?.event_id ?? String(eventId),
    my: data?.my ?? null,
    positive: Number(data?.positive ?? 0),
    negative: Number(data?.negative ?? 0),
  };
}

/**
 * Поставить/обновить мою оценку мероприятию
 * review: "positive" | "negative"
 */
export async function setEventFeedback(eventId, review) {
  const res = await axiosInstance.post(
    EVENT_FEEDBACK_API,
    { event_id: eventId, review },
    { headers: getAuthHeaders() }
  );
  return res.data;
}

/**
 * Убрать мою оценку мероприятия
 */
export async function deleteEventFeedback(eventId) {
  const res = await axiosInstance.delete(
    `${EVENT_FEEDBACK_API}${String(eventId)}`,
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

export async function getUserFeedback(userId) {
  const { data } = await axiosInstance.get(
    `${FEEDBACK_API}${String(userId)}`,
    { headers: getAuthHeaders() }
  );

  // Ожидаем форму:
  // { user_id, my: "positive"|"negative"|null, positive: number, negative: number }
  return {
    user_id: data?.user_id ?? String(userId),
    my: data?.my ?? null,
    positive: Number(data?.positive ?? 0),
    negative: Number(data?.negative ?? 0),
  };

}

export async function getUserEventsFeedback(userId) {
  const { data } = await axiosInstance.get(
    `${FEEDBACK_API}events/${String(userId)}`,
    { headers: getAuthHeaders() }
  );

  return {
    user_id: data?.user_id ?? String(userId),
    positive: Number(data?.positive ?? 0),
    negative: Number(data?.negative ?? 0),
  };
}
