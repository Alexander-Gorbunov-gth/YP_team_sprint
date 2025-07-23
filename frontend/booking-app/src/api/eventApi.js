import axios from 'axios';
import { API_BASE } from '../config';

export async function getEvents() {
//   const res = await axios.get(`${API_BASE}/events`);
//   return res.data;
    return {
        "events": [
            {
                "id": 1,
                "movie_id": 1,
                "address_id": 1,
                "capacity": 100,
                "start_datetime": "2023-10-01T18:00:00Z"
            },
            {
                "id": 2,
                "movie_id": 2,
                "address_id": 2,
                "capacity": 150,
                "start_datetime": "2023-10-02T20:00:00Z"
            }
        ]
    };
}
