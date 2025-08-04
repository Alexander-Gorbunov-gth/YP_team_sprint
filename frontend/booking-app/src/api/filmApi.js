import axios from './axiosInstance'; 
import { FILM_SERVICE_BASE_URL } from '../config';
import { getAuthHeaders } from "./authHeaders";
import axiosInstance from "./axiosInstance";

export async function searchFilms(query) {
  try {
    const res = await axiosInstance.get(`${FILM_SERVICE_BASE_URL}/films/search/`, {
      params: {
        query: query,
        page_size: 10
      }
    });
    return res.data;
  } catch (error) {
    console.error("Ошибка при поиске фильмов:", error);
    return [];
  }
}   