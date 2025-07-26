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
        }
    };
}