import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getBookingById, updateBookingStatus } from "../../api/bookingApi";
import styles from "./BookingDetailPage.module.css";

export default function BookingDetailPage() {
  const { id } = useParams();
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getBookingById(id)
      .then((data) => setBooking(data))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p>Загрузка...</p>;
  if (!booking) return <p>Бронирование не найдено</p>;

  const movie = booking.movie || {};

  function renderStatus(status) {
    switch (status) {
      case "pending":
        return "Ожидает подтверждения автора";
      case "success":
        return "Подтверждено";
      case "canceled":
        return "Отменено";
      default:
        return status;
    }
  }

  async function handleUpdateStatus(newStatus) {
    try {
      await updateBookingStatus(booking.id, newStatus);
      setBooking({ ...booking, status: newStatus });
    } catch (error) {
      alert("Не удалось обновить статус");
    }
  }

  return (
    <div className={styles.container}>
      <h2>Бронирование #{booking.id}</h2>
      <p><strong>Фильм:</strong> {movie.title}</p>
      <p><strong>Жанры:</strong> {movie.genres?.join(", ") || "–"}</p>
      <p><strong>Режиссёры:</strong> {movie.directors_names?.join(", ") || "–"}</p>
      <p><strong>Актёры:</strong> {movie.actors_names?.join(", ") || "–"}</p>
      <p><strong>Количество мест:</strong> {booking.seats}</p>
      <p><strong>Статус:</strong> {renderStatus(booking.status)}</p>
      {booking.status === "success" || booking.status === "pending" && (
        <button
          className={styles.buttonCancel}
          onClick={() => handleUpdateStatus("canceled")}
        >
          Отменить бронирование
        </button>
      )}
    </div>
  );
}