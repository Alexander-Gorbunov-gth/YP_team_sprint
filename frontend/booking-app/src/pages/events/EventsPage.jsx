import { useEffect, useState } from "react";
import { getEvents } from "../../api/eventApi";
import { createSubscription, getMySubscriptions } from "../../api/subscriptionApi";
import dayjs from "dayjs";
import { Link, useNavigate } from "react-router-dom";
import styles from "./EventsPage.module.css";

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [mySubscriptions, setMySubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const offset = 0;
    const limit = 20;
    Promise.all([getEvents({ offset, limit }), getMySubscriptions()])
      .then(([eventData, subscriptionsData]) => {
        setEvents(eventData);
        console.log("Подписки пользователя:", subscriptionsData);
        setMySubscriptions(subscriptionsData || []);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Загрузка событий...</p>;
  if (!events.length) return <p>Нет доступных событий.</p>;



  return (
    <div className={styles.container}>
      {/* <h2 className={styles.title}>Доступные события</h2> */}
      {events.map((event) => (
        <EventCard key={event.id} event={event} mySubscriptions={mySubscriptions} />
      ))}
    </div>
  );
}

function EventCard({ event, mySubscriptions }) {
  const navigate = useNavigate();

  const movie = event.movie || {};

  const isSubscribed = mySubscriptions.some(sub => sub.host_id === event.author?.id);

  return (
    <div className={styles.card}>
      <h3>{movie.title || `Событие #${event.id}`}</h3>
      <p><strong>Дата:</strong> {dayjs(event.start_datetime).format("DD.MM.YYYY HH:mm")}</p>
      <p><strong>Адрес:</strong> {event.address}</p>
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
      {event.author && (
        <div className={styles.authorInfo}>
          <p><strong>Автор:</strong> {event.author.username}</p>
        </div>
      )}
      <div className={styles.actions}>
        
        <Link to={`/bookings/new?event_id=${event.id}`} className={styles.button}>
          Посетить мероприятие
        </Link>
        {!isSubscribed && (
          <button
            className={styles.subscribeButton}
            onClick={async () => {
              try {
                await createSubscription({
                  host_id: event.author?.id,
                });
                navigate(0); // Обновить страницу
              } catch (err) {
                console.error("Ошибка подписки", err);
                alert("Не удалось подписаться");
              }
            }}
          >
            Подписаться на события автора
          </button>
        )}
      </div>
    </div>
  );
}