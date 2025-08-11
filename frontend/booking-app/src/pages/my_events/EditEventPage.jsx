import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getEventById, updateEvent } from "../../api/eventApi";
import { getMyAddresses } from "../../api/addressApi";
import { getBookingById, updateBookingStatus } from "../../api/bookingApi";
import { FaThumbsUp, FaThumbsDown } from "react-icons/fa";
import { createUserFeedback } from "../../api/userFeedbackApi";
import styles from "./EditEventPage.module.css";

export default function EditEventPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [event, setEvent] = useState(null);
  const [addresses, setAddresses] = useState([]);
  const [form, setForm] = useState({});
  const [loading, setLoading] = useState(true);

  const [actionLoadingId, setActionLoadingId] = useState(null);

  const handleFeedback = async (user_id, review) => {
    await createUserFeedback({ user_id, review });
    // Success notifications (if any) handled elsewhere; errors handled by global interceptor
  };

  const refreshEvent = async () => {
    const fresh = await getEventById(id);
    setEvent(fresh);
  };

  const handleConfirm = async (reservationId) => {
    setActionLoadingId(reservationId);
    try {
      await updateBookingStatus(reservationId, "success");
      await refreshEvent();
    } finally {
      setActionLoadingId(null);
    }
  };
  const handleCancel = async (reservationId) => {
    setActionLoadingId(reservationId);
    try {
      await updateBookingStatus(reservationId, "canceled");
      await refreshEvent();
    } finally {
      setActionLoadingId(null);
    }
  };

  useEffect(() => {
    Promise.all([getEventById(id), getMyAddresses()])
      .then(([eventData, addressData]) => {
        setEvent(eventData);
        setAddresses(addressData);
        setForm({
        //   movie_id: eventData.movie_id,
          address_id: eventData.address_id,
          capacity: eventData.capacity,
          start_datetime: eventData.start_datetime,
        });
        console.log(eventData)
      })
      .finally(() => setLoading(false));
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await updateEvent(id, form);
    navigate("/my-events");
  };

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

  if (loading) return <p>Загрузка...</p>;
  if (!event) return <p>Мероприятие не найдено</p>;
  const movie = event.movie || {};
  const POSITIVE = "positive";
  const NEGATIVE = "negative";
  
  return (
    <div className={styles.container}>
      <div className={styles.twoCols}>
        {/* Left: Reservations list */}
        <div className={styles.col}>
          <h2 className={styles.colTitle}>Брони по событию</h2>
          {Array.isArray(event.reservations) && event.reservations.length > 0 ? (
            <div>
              {event.reservations.map((r) => (
                <div key={r.id} className={styles.bookingCard}>
                  <div className={styles.bookingDetails}>
                    <div><strong>Бронировал:</strong> {r.author?.username ?? "—"}</div>
                    <div><strong>Мест:</strong> {r.seats}</div>
                    <div><strong>Статус:</strong> {renderStatus(r.status)}</div>
                    {r.author?.id !== event.author?.id && (
                      <div style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
                        <FaThumbsUp
                          style={{ cursor: "pointer", color: "#10b981", fontSize: "20px" }}
                          onClick={() => handleFeedback(r.author?.id, POSITIVE)}
                          title="Поставить лайк"
                        />
                        <FaThumbsDown
                          style={{ cursor: "pointer", color: "#ef4444", fontSize: "20px" }}
                          onClick={() => handleFeedback(r.author?.id, NEGATIVE)}
                          title="Поставить дизлайк"
                        />
                      </div>
                    )}
                  </div>
                  <div className={styles.buttonGroup}>
                    {r.status !== "success" && r.status !== "canceled" && (
                      <button
                        type="button"
                        onClick={() => handleConfirm(r.id)}
                        disabled={actionLoadingId === r.id}
                        className={styles.buttonConfirm}
                      >
                        Подтвердить
                      </button>
                    )}
                    {r.status !== "canceled" && (
                      <button
                        type="button"
                        onClick={() => handleCancel(r.id)}
                        disabled={actionLoadingId === r.id}
                        className={styles.buttonCancel}
                      >
                        Отменить
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p>Пока нет броней</p>
          )}
        </div>

        {/* Right: Form + Movie info */}
        <div className={styles.col}>
          <h2 className={styles.colTitle}>Редактировать мероприятие</h2>
          <div className={styles.movieInfo}>
            <h3>{movie.title}</h3>
            <p><strong>Жанры:</strong> {movie.genres?.join(", ") || "–"}</p>
            <p><strong>Описание:</strong> {movie.description || "–"}</p>
            <p><strong>Режиссёры:</strong> {movie.directors_names?.join(", ") || "–"}</p>
            <p><strong>Актёры:</strong> {movie.actors_names?.join(", ") || "–"}</p>
          </div>
          <form onSubmit={handleSubmit} className={styles.form}>
            <label className={styles.label}>
              Адрес:
              <select
                name="address_id"
                className={styles.input}
                value={form.address_id}
                onChange={handleChange}
                required
              >
                <option value="">Выберите адрес</option>
                {addresses.map((addr) => (
                  <option key={addr.id} value={addr.id}>
                    {addr.city}, {addr.street} {addr.house}
                  </option>
                ))}
              </select>
            </label>

            <label className={styles.label}>
              Вместимость:
              <input
                type="number"
                name="capacity"
                className={styles.input}
                value={form.capacity}
                onChange={handleChange}
                required
              />
            </label>

            <label className={styles.label}>
              Дата и время:
              <input
                type="datetime-local"
                name="start_datetime"
                className={styles.input}
                value={(form.start_datetime || "").slice(0, 16)}
                onChange={handleChange}
                required
              />
            </label>

            <button type="submit" className={styles.button}>Сохранить</button>
          </form>
        </div>
      </div>
    </div>
  );
}