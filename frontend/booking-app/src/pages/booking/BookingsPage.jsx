import { useEffect, useState } from "react";
import { getBookingsByUser } from "../../api/bookingApi";
import { useNavigate, useSearchParams } from "react-router-dom";
import styles from "./BookingsPage.module.css";

export default function BookingsPage() {
  function getStatusLabel(status) {
    switch (status) {
      case "pending":
        return "Забронировано";
      case "canceled":
        return "Отменено";
      case "success":
        return "Подтверждено";
      default:
        return status;
    }
  }
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const eventIdFilter = searchParams.get("event_id");
  const navigate = useNavigate();

  useEffect(() => {
    getBookingsByUser() // заменишь на реальный user_id
      .then((data) => {
        const allBookings = Array.isArray(data.bookings) ? data.bookings : data;
        const filtered = eventIdFilter
          ? allBookings.filter((b) => b.event_id === eventIdFilter)
          : allBookings;
        setBookings(filtered);
      })
      .finally(() => setLoading(false));
  }, [eventIdFilter]);

  if (loading) return <p>Загрузка...</p>;
  if (!bookings.length) return <p>Бронирований пока нет</p>;

  return (
    <div className={styles.container}>
      <h2>Мои бронирования</h2>
      {bookings.map((b) => (
        <div
          key={b.id}
          className={styles.card}
          // onClick={() => navigate(`/bookings/${b.id}`)}
        >
          <p><strong>Мероприятие:</strong> {b.movie_title || b.event_id}</p>
          <p><strong>Мест:</strong> {b.seats}</p>
          <p><strong>Статус:</strong> {getStatusLabel(b.status)}</p>

          {b.status !== "canceled" && (
            <button
              className={styles.button}
              onClick={(e) => {
                e.stopPropagation();
                navigate(`/bookings/${b.id}`);
              }}
            >
              Управлять бронированием
            </button>
          )}
          
        </div>
      ))}
    </div>
  );
}