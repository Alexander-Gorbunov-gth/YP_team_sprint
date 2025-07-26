import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getEventById, updateEvent } from "../../api/eventApi";
import { getMyAddresses } from "../../api/addressApi";
import styles from "./CreateEventPage.module.css";

export default function EditEventPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [event, setEvent] = useState(null);
  const [addresses, setAddresses] = useState([]);
  const [form, setForm] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getEventById(id), getMyAddresses()])
      .then(([eventData, addressData]) => {
        setEvent(eventData);
        setAddresses(addressData);
        setForm({
          movie_id: eventData.movie_id,
          address_id: eventData.address_id,
          capacity: eventData.capacity,
          start_datetime: eventData.start_datetime,
        });
      })
      .finally(() => setLoading(false));
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateEvent(id, form);
      navigate("/my-events");
    } catch (err) {
      alert("Ошибка при обновлении мероприятия");
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (!event) return <p>Мероприятие не найдено</p>;
  const movie = event.movie || {};

  return (
    <div className={styles.container}>
      <h2>Редактировать мероприятие</h2>
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
            value={form.start_datetime.slice(0, 16)}
            onChange={handleChange}
            required
          />
        </label>

        <button type="submit" className={styles.button}>Сохранить</button>
      </form>
    </div>
  );
}