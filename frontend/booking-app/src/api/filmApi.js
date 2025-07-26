import axios from 'axios';
import { FILM_SERVICE_BASE_URL } from '../config';

export async function searchFilms(query) {
  try {
    const res = await axios.get(`${FILM_SERVICE_BASE_URL}/films/search/`, {
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