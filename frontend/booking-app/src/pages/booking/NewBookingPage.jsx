import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { getEventById } from "../../api/eventApi";
import { createReservation } from "../../api/bookingApi";
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

  useEffect(() => {
    if (eventId) {
      getEventById(eventId)
        .then(setEvent)
        .finally(() => setLoading(false));
    }
  }, [eventId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const newReservation = await createReservation({
        event_id: event.id,
        seats: Number(seats),
        status: "pending",
      });
      navigate(`/bookings/${newReservation.id}`);
    } catch {
      alert("Ошибка при бронировании");
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (!event) return <p>Мероприятие не найдено</p>;

  const address = event.address
    ? `${event.address.city}, ${event.address.street} ${event.address.house}`
    : "Адрес не указан";

  const movie = event.movie || {};
  const availableSeats = event.reservations ? event.capacity - event.reservations.length : event.capacity;

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
      <p><strong>Свободных мест:</strong> {availableSeats}</p>

      <hr style={{ margin: "20px 0" }} />

      <form onSubmit={handleSubmit}>
        <label>
          Количество мест:
          <input
            type="number"
            min="1"
            max={event.capacity}
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