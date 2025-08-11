import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { getEventById, createEventReserv } from "../../api/eventApi";
import { getUserFeedback, getUserEventsFeedback } from "../../api/userFeedbackApi";
import dayjs from "dayjs";
import styles from "./NewBookingPage.module.css";

export default function NewBookingPage() {
  const [searchParams] = useSearchParams();
  const eventId = searchParams.get("event_id");
  const navigate = useNavigate();

  const [event, setEvent] = useState(null);
  const [seats, setSeats] = useState(1);
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState(false);
  const [authorFeedback, setAuthorFeedback] = useState(null);
  const [authorEventsFeedback, setAuthorEventsFeedback] = useState(null);

  useEffect(() => {
    if (eventId) {
      getEventById(eventId)
        .then((eventData) => {
          setEvent(eventData);
          if (eventData && eventData.author && eventData.author.id) {
            getUserFeedback(eventData.author.id).then(setAuthorFeedback);
            getUserEventsFeedback(eventData.author.id).then(setAuthorEventsFeedback);
          }
        })
        .finally(() => setLoading(false));
    }
  }, [eventId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newReservation = await createEventReserv(event.id, Number(seats));
      navigate(`/bookings/${newReservation.id}`);
    } catch (e) {
      // Error shown by global axios interceptor
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (!event) return <p>Мероприятие не найдено</p>;

  const address = event.address
    ? `${event.address.city}, ${event.address.street} ${event.address.house}`
    : "Адрес не указан";

  const movie = event.movie || {};

  return (
    <div className={styles.container}>
      <h2>{movie.title}</h2>
      <p><strong>Жанры:</strong> {movie.genres?.join(", ")}</p>
      <p><strong>Режиссёр(ы):</strong> {movie.directors_names?.join(", ")}</p>
      <p><strong>Актёры:</strong> {movie.actors_names?.join(", ")}</p>
      <p><strong>Описание:</strong> {movie.description || "–"}</p>

      <p><strong>Дата:</strong> {dayjs(event.start_datetime).format("DD.MM.YYYY HH:mm")}</p>
      <p><strong>Адрес:</strong> {`${event.address}`}</p>
      <p><strong>Вместимость:</strong> {event.capacity}</p>
      <p><strong>Свободных мест:</strong> {event.available_seats}</p>

      <div style={{ margin: "20px 0", padding: "10px", border: "1px solid #ccc", borderRadius: "4px" }}>
        <p><strong>Оценки автора:</strong> 👍 {authorFeedback?.positive ?? 0} / 👎 {authorFeedback?.negative ?? 0}</p>
        <p><strong>Оценки событий автора:</strong> 👍 {authorEventsFeedback?.positive ?? 0} / 👎 {authorEventsFeedback?.negative ?? 0}</p>
      </div>

      <hr style={{ margin: "20px 0" }} />

      <form onSubmit={handleSubmit}>
        <label>
          Количество мест:
          <input
            type="number"
            min="1"
            // max={Math.max(1, event.available_seats ?? event.capacity)}
            value={seats}
            onChange={(e) => setSeats(e.target.value)}
            required
            className={styles.input}
          />
        </label>
        <div style={{ marginTop: "16px" }}>
          <button type="submit" className={styles.button}>
            Забронировать
          </button>
        </div>
      </form>
    </div>
  );
}