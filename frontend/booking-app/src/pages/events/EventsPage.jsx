import { useEffect, useState } from "react";
import { getEvents } from "../../api/eventApi";
import dayjs from "dayjs";
import { Link } from "react-router-dom";
import styles from "./EventsPage.module.css";

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEvents()
      .then((data) => setEvents(data.events))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Загрузка событий...</p>;
  if (!events.length) return <p>Нет доступных событий.</p>;

  return (
    <div className={styles.container}>
      {/* <h2 className={styles.title}>Доступные события</h2> */}
      {events.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  );
}

function EventCard({ event }) {
  const address = event.address
    ? `${event.address.city}, ${event.address.street} ${event.address.house}` +
      (event.address.flat ? `, кв. ${event.address.flat}` : "")
    : "Адрес не указан";

  const movie = event.movie || {};

  return (
    <div className={styles.card}>
      <h3>{movie.title || `Событие #${event.id}`}</h3>
      <p><strong>Дата:</strong> {dayjs(event.start_datetime).format("DD.MM.YYYY HH:mm")}</p>
      <p><strong>Адрес:</strong> {address}</p>
      <p><strong>Вместимость:</strong> {event.capacity}</p>
      {movie.genres?.length > 0 && (
        <p><strong>Жанры:</strong> {movie.genres.join(", ")}</p>
      )}
      {movie.directors_names?.length > 0 && (
        <p><strong>Режиссёр:</strong> {movie.directors_names.join(", ")}</p>
      )}
      {movie.actors_names?.length > 0 && (
        <p><strong>Актёры:</strong> {movie.actors_names.join(", ")}</p>
      )}
      {movie.description && (
        <p><strong>Описание:</strong> {movie.description}</p>
      )}
      <Link to={`/bookings/new?event_id=${event.id}`} className={styles.button}>
        Посетить мероприятие
      </Link>
    </div>
  );
}