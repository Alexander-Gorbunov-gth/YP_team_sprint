import axios from 'axios';
import { API_BASE } from '../config';


export async function createReservation(payload) {
  const res = await axios.post(`${API_BASE}/reservation/`, payload);
  return res.data;
    // return {
    //     id: "uuid-r1",
    //     user_id: "uuid-u1",
    //     event_id: payload.event_id,
    //     seats: payload.seats,
    //     status: payload.status,
    //     created_at: new Date().toISOString(),
    // };
}

export async function getBookingsByUser() {
  // Пример заглушки — заменить на реальный API-запрос при подключении backend
  return {
    bookings: [
      {
        id: "uuid-b1",
        // user_id: userId,
        event_id: "uuid-e1",
        seats: 2,
        status: "SUCCESS",
        created_at: "2023-10-01T18:00:00Z",
        event: {
          movie: {
            title: "Война и мир",
          }
        }
      },
      {
        id: "uuid-b2",
        // user_id: userId,
        event_id: "uuid-e2",
        seats: 1,
        status: "PENDING",
        created_at: "2023-10-02T20:00:00Z",
        event: {
          movie: {
            title: "Дюна",
          }
        }
      }
    ]
  };
}


export async function getBookingById(id) {
  const res = await axios.get(`${API_BASE}/reservation/${id}`);
  return res.data;

    // return {
    //     "id": "e68f1a5a-3d65-4b98-b0a2-b36e3d4c4c5a",
    //     "event_id": "b0d535c1-26fc-4a4a-a206-189e9e6e0721",
    //     "seats": 2,
    //     "status": "PENDING",
    //     "movie": {
    //         "genres": ["драма", "история"],
    //         "title": "Война и мир",
    //         "description": "Экранизация великого романа.",
    //         "directors_names": ["Сергей Бондарчук"],
    //         "actors_names": ["Людмила Савельева", "Вячеслав Тихонов"]
    //     }
    // }
    
}
export async function updateBookingStatus(id, newStatus) {
  console.log("Updating booking status:", id, newStatus);
  const res = await axios.patch(`${API_BASE}/reservation/${id}`, { status: newStatus });
  return res.data;
}
