import axios from 'axios';
import { API_BASE } from '../config';

export async function getEvents() {
//   const res = await axios.get(`${API_BASE}/events`);
//   return res.data;
    return {
        events: [
            {
            id: 1,
            movie_id: "uuid-1",
            address_id: "uuid-a1",
            owner_id: "uuid-o112",
            capacity: 100,
            start_datetime: "2023-10-01T18:00:00Z",
            address: {
                id: "uuid-a1",
                country: "Россия",
                city: "Москва",
                street: "Тверская",
                house: "10",
                flat: null
            },
            movie: {
                genres: ["драма", "история"],
                title: "Война и мир",
                description: "Экранизация великого романа.",
                directors_names: ["Сергей Бондарчук"],
                actors_names: ["Людмила Савельева", "Вячеслав Тихонов"]
            },
            author: {
                id: "uuid-o112",
                name: "Иван Иванов",
                username: "ivanov"
            }
            },
            {
            id: 2,
            movie_id: "uuid-2",
            address_id: "uuid-a2",
            owner_id: "uuid-o2",
            capacity: 150,
            start_datetime: "2023-10-02T20:00:00Z",
            address: {
                id: "uuid-a2",
                country: "Россия",
                city: "Санкт-Петербург",
                street: "Невский проспект",
                house: "25",
                flat: "3"
            },
            movie: {
                genres: ["комедия"],
                title: "Бриллиантовая рука",
                description: "Легендарная советская комедия.",
                directors_names: ["Леонид Гайдай"],
                actors_names: ["Юрий Никулин", "Андрей Миронов"]
            },
            author: {
                id: "uuid-o1",
                name: "Иван Иванов",
                username: "ivanov"
            }
            }
        ]
    };
}


export async function getEventById(id) {
//   const res = await axios.get(`${API_BASE}/events/${id}`);
//   return res.data;
    return {
        id: 1,
        movie_id: "uuid-1",
        address_id: "uuid-a1",
        owner_id: "uuid-o1",
        capacity: 100,
        start_datetime: "2023-10-01T18:00:00Z",
        address: {
        id: "uuid-a1",
        country: "Россия",
        city: "Москва",
        street: "Тверская",
        house: "10",
        flat: null
        },
        movie: {
        genres: ["драма", "история"],
        title: "Война и мир",
        description: "Экранизация великого романа.",
        directors_names: ["Сергей Бондарчук"],
        actors_names: ["Людмила Савельева", "Вячеслав Тихонов"]
        },
        author: {
                id: "uuid-o1",
                name: "Иван Иванов",
                username: "ivanov"
            }
    };
}



export async function getMyEvents() {
  return {
    events: [
      {
        id: 1,
        movie_id: "uuid-1",
        address_id: "uuid-a1",
        owner_id: "00000000-0000-0000-0000-000000000001",
        capacity: 100,
        start_datetime: "2023-10-01T18:00:00Z",
        address: {
          id: "uuid-a1",
          country: "Россия",
          city: "Москва",
          street: "Тверская",
          house: "10",
          flat: null
        },
        movie: {
          genres: ["драма", "история"],
          title: "Война и мир",
          description: "Экранизация великого романа.",
          directors_names: ["Сергей Бондарчук"],
          actors_names: ["Людмила Савельева", "Вячеслав Тихонов"]
        },
        status: "active"
      },
      {
        id: 2,
        movie_id: "uuid-2",
        address_id: "uuid-a2",
        owner_id: "00000000-0000-0000-0000-000000000001",
        capacity: 80,
        start_datetime: "2023-11-10T16:00:00Z",
        address: {
          id: "uuid-a2",
          country: "Россия",
          city: "Казань",
          street: "Баумана",
          house: "12",
          flat: null
        },
        movie: {
          genres: ["триллер"],
          title: "Тайна на Волге",
          description: "Захватывающий детектив.",
          directors_names: ["Иван Иванов"],
          actors_names: ["Анна Смирнова", "Дмитрий Петров"]
        },
        status: "finished"
      }
    ]
  };
}

export async function createEvent(eventData) {
  try {
    const res = await axios.post(`${API_BASE}/events`, eventData);
    return res.data;
  } catch (error) {
    console.error("Ошибка при создании события:", error);
    throw error;
  }
}

export async function updateEvent(id, data) {
  const res = await axios.patch(`${API_BASE}/events/${id}`, data);
  return res.data;
}