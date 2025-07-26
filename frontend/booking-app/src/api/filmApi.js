import axios from 'axios';
import { API_BASE } from '../config';

export async function searchFilms(query) {
  try {
    const res = await axios.get(`${API_BASE}/films/search/`, {
      params: {
        query,
        page_size: 10
      }
    });
    return res.data;
  } catch (error) {
    console.error("Ошибка при поиске фильмов:", error);
    return [];
  }
}   