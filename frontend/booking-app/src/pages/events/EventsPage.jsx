import { useEffect, useState } from "react";
import { getEvents } from "../../api/eventApi";
import dayjs from "dayjs";
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
      <h2 className={styles.title}>Доступные события</h2>
      {events.map((event) => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  );
}

function EventCard({ event }) {
  const address = event.address
    ? `${event.address.city}, ${event.address.street} ${event.address.house}`
    : "Адрес не указан";

  return (
    <div className={styles.card}>
      <h3>Событие #{event.id}</h3>
      <p><strong>Фильм:</strong> {event.movie_id}</p>
      <p><strong>Адрес:</strong> {address}</p>
      <p><strong>Вместимость:</strong> {event.capacity}</p>
      <p><strong>Начало:</strong> {dayjs(event.start_datetime).format("DD.MM.YYYY HH:mm")}</p>
    </div>
  );
}