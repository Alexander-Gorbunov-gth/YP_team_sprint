import { useEffect, useState } from "react";
import { getEvents, getNearbyEvents } from "../../api/eventApi";
import { getMyAddresses } from "../../api/addressApi";
import { createSubscription, getMySubscriptions } from "../../api/subscriptionApi";
import { getUserFeedback, getUserEventsFeedback } from "../../api/userFeedbackApi";
import dayjs from "dayjs";
import { Link, useNavigate } from "react-router-dom";
import styles from "./EventsPage.module.css";

export default function EventsPage() {
  const [events, setEvents] = useState([]);
  const [mySubscriptions, setMySubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  const [addresses, setAddresses] = useState([]);
  const [selectedAddressId, setSelectedAddressId] = useState("");
  const [radiusKm, setRadiusKm] = useState(5);
  const [filteredEvents, setFilteredEvents] = useState(null); // null -> not filtered
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    const offset = 0;
    const limit = 20;
    Promise.all([
      getEvents({ offset, limit }),
      getMySubscriptions(),
      getMyAddresses(),
    ])
      .then(([eventData, subscriptionsData, myAddresses]) => {
        setEvents(eventData);
        setMySubscriptions(subscriptionsData || []);
        setAddresses(myAddresses || []);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleNearbySearch = async (e) => {
    e?.preventDefault?.();
    if (!selectedAddressId) return;
    try {
      setSearching(true);
      const data = await getNearbyEvents({ addressId: selectedAddressId, radiusKm });
      setFilteredEvents(Array.isArray(data) ? data : []);
    } finally {
      setSearching(false);
    }
  };

  const handleResetFilter = () => {
    setFilteredEvents(null);
  };

  if (loading) return <p>Загрузка событий...</p>;
  const list = filteredEvents !== null ? filteredEvents : events;
  if (!list.length) return <p>Нет доступных событий.</p>;

  return (
    <div style={{ width: "100%" }}>
      {/* Full-width search bar */}
      <div
        className={styles.filterBar}
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 12,
          marginBottom: 20,
          border: "1px solid #e5e7eb",
          padding: 12,
          borderRadius: 10,
          background: "#fff",
          width: "100%",
          maxWidth: 800,
          marginLeft: "auto",
          marginRight: "auto",
          flexWrap: "wrap",
        }}
      >
        <h3 style={{ width: "100%", textAlign: "center", marginBottom: 12 }}>
          Найти события рядом
        </h3>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 12,
            flexWrap: "wrap",
            width: "100%",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <label
              style={{
                fontSize: 12,
                color: "#6b7280",
                marginBottom: 6,
                textAlign: "center",
              }}
            >
              Сохранённый адрес
            </label>
            <select
              value={selectedAddressId}
              onChange={(e) => setSelectedAddressId(e.target.value)}
              className={styles.select}
              style={{
                width: "340px",
                padding: "8px 10px",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                textAlign: "center",
              }}
            >
              <option value="">— Выберите адрес —</option>
              {addresses.map((addr) => (
                <option key={addr.id} value={addr.id}>
                   {addr.city}, {addr.street} {addr.house}
                </option>
              ))}
            </select>
          </div>

          <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <label
              style={{
                fontSize: 12,
                color: "#6b7280",
                marginBottom: 6,
                textAlign: "center",
              }}
            >
              Радиус (км)
            </label>
            <input
              type="number"
              min={1}
              step={0.5}
              value={radiusKm}
              onChange={(e) => setRadiusKm(Number(e.target.value) || 1)}
              className={styles.input}
              style={{
                width: "60px",
                padding: "8px 10px",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                textAlign: "center",
              }}
            />
          </div>

          <button
            onClick={handleNearbySearch}
            disabled={!selectedAddressId || searching}
            className={styles.button}
            style={{ padding: "10px 14px" }}
          >
            {searching ? "Ищем..." : "Показать рядом"}
          </button>

          {filteredEvents !== null && (
            <button
              onClick={handleResetFilter}
              className={styles.button}
              style={{ padding: "10px 14px", background: "#6b7280" }}
            >
              Сбросить
            </button>
          )}
        </div>
      </div>

      {/* Cards container under the full-width filter */}
      <div className={styles.container}>
      {list.map((event) => (
        <EventCard key={event.id} event={event} mySubscriptions={mySubscriptions} />
      ))}
      </div>
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
      {/* {movie.description && (
        <p><strong>Описание:</strong> {movie.description}</p>
      )} */}
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
            className={styles.buttonSecondary}
            onClick={async () => {
              try {
                await createSubscription({
                  host_id: event.author?.id,
                });
                navigate(0); // Обновить страницу
              } catch (err) {
                console.error("Ошибка подписки", err);
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