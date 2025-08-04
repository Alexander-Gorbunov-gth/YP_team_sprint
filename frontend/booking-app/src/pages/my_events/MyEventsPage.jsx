import { useEffect, useState } from "react";
import { getMyEvents } from "../../api/eventApi";
import { useNavigate } from "react-router-dom";
import styles from "./MyEventsPage.module.css";

export default function MyEventsPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    getMyEvents()
      .then((data) => {
        setEvents(data);
        console.log("Полученные мероприятия:", data);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (!events.length)
    return (
      <div className={styles.container}>
        <h2>Мои мероприятия</h2>
        <p>Вы пока не создали ни одного мероприятия.</p>
        <div>
          <button
            className={styles.createButton}
            onClick={() => navigate("/events/new")}
          >
            Создать мероприятие
          </button>
          <button
            className={styles.secondaryButton}
            onClick={() => navigate("/addresses/new")}
            style={{ marginLeft: "10px" }}
          >
            Добавить адрес
          </button>
        </div>
      </div>
    );

  return (
    
    <div className={styles.container}>
      <div className={styles.headerRow}>
        <h2>Мои мероприятия</h2>
        <div>
          <button
            className={styles.createButton}
            onClick={() => navigate("/events/new")}
          >
            Создать мероприятие
          </button>
          <button
            className={styles.secondaryButton}
            onClick={() => navigate("/addresses/new")}
            style={{ marginLeft: "10px" }}
          >
            Добавить адрес
          </button>
        </div>
      </div>
      <div className={styles.grid}>
        {events.map((event) => (
          <div
            key={event.id}
            className={styles.card}
            onClick={() => navigate(`/events/${event.id}`)}
            style={{ cursor: "pointer" }}
          >
            <h3>{event.movie?.title || "Название неизвестно"}</h3>
            <p>
              <strong>Адрес:</strong> {event.address}
            </p>
            <p>
              <strong>Статус:</strong> {new Date(event.start_datetime) > new Date() ? "Запланировано" : "Завершено"}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}