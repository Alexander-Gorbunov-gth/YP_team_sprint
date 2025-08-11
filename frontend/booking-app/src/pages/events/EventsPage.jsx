import { useEffect, useState } from "react";
import { getEvents } from "../../api/eventApi";
import { createSubscription, getMySubscriptions } from "../../api/subscriptionApi";
import { getUserFeedback, getUserEventsFeedback } from "../../api/userFeedbackApi";
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

  const [authorFeedback, setAuthorFeedback] = useState({ positive: 0, negative: 0, my: null });
  const [eventsFeedback, setEventsFeedback] = useState({ positive: 0, negative: 0 });
  const [feedbackLoading, setFeedbackLoading] = useState(true);

  const movie = event.movie || {};

  const isSubscribed = mySubscriptions.some(sub => sub.host_id === event.author?.id);

  useEffect(() => {
    const authorId = event.author?.id;
    if (!authorId) {
      setFeedbackLoading(false);
      return;
    }
    let isMounted = true;
    (async () => {
      try {
        const data = await getUserFeedback(authorId);
        // Expected shape: { user_id, my, positive, negative }
        if (isMounted && data) {
          setAuthorFeedback({
            positive: Number(data.positive ?? 0),
            negative: Number(data.negative ?? 0),
            my: data.my ?? null,
          });
        }

        // Fetch overall events feedback for this author
        const eventsData = await getUserEventsFeedback(authorId);
        if (isMounted && eventsData) {
          setEventsFeedback({
            positive: Number(eventsData.positive ?? 0),
            negative: Number(eventsData.negative ?? 0),
          });
        }
      } catch (e) {
        // silently ignore on list page
      } finally {
        if (isMounted) setFeedbackLoading(false);
      }
    })();
    return () => { isMounted = false; };
  }, [event.author?.id]);

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
          <p><strong>Автор:</strong> {event.author.username} ( 👍 {authorFeedback.positive} / 👎 {authorFeedback.negative} )</p>
          <div className={styles.authorFeedback}>
          
          </div>
          <div className={styles.authorFeedback} style={{ marginTop: 6 }}>
            <p><strong>Оценки событий автора:</strong></p>
            <span title="Лайки за события автора">👍 {eventsFeedback.positive}</span>
            <span style={{ marginLeft: 10 }} title="Дизлайки за события автора">👎 {eventsFeedback.negative}</span>
          </div>
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