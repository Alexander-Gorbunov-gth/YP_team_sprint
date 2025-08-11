import { useEffect, useMemo, useState } from "react";
import { getBookingsByUser } from "../../api/bookingApi";
import { useNavigate, useSearchParams } from "react-router-dom";
import { FaThumbsUp, FaThumbsDown } from "react-icons/fa";
import { getEventFeedback, setEventFeedback, deleteEventFeedback } from "../../api/userFeedbackApi";
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

  // feedbackByEvent: { [eventId]: { my: 'positive'|'negative'|null, positive: number, negative: number } }
  const [feedbackByEvent, setFeedbackByEvent] = useState({});

  const POSITIVE = "positive";
  const NEGATIVE = "negative";

  const applyFeedbackLocal = (eventId, nextMy) => {
    setFeedbackByEvent((prev) => {
      const cur = prev[eventId] || { my: null, positive: 0, negative: 0 };
      let { my, positive, negative } = cur;

      // remove previous mark
      if (my === POSITIVE) positive = Math.max(0, positive - 1);
      if (my === NEGATIVE) negative = Math.max(0, negative - 1);

      // add new mark (if not null)
      if (nextMy === POSITIVE) positive += 1;
      if (nextMy === NEGATIVE) negative += 1;

      return { ...prev, [eventId]: { my: nextMy, positive, negative } };
    });
  };

  const handleEventFeedback = async (eventId, type) => {
    const current = feedbackByEvent[eventId]?.my ?? null;
    try {
      if (current === type) {
        // toggle off
        await deleteEventFeedback(eventId);
        applyFeedbackLocal(eventId, null);
      } else {
        await setEventFeedback(eventId, type);
        applyFeedbackLocal(eventId, type);
      }
    } catch (_) {
      // errors are handled by global axios interceptor / toasts
    }
  };

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        const data = await getBookingsByUser();
        const allBookings = Array.isArray(data.bookings) ? data.bookings : data;
        const filtered = eventIdFilter
          ? allBookings.filter((b) => b.event_id === eventIdFilter)
          : allBookings;
        if (!mounted) return;
        setBookings(filtered);

        // Fetch feedback for unique event ids
        const ids = Array.from(new Set(filtered.map((b) => b.event_id).filter(Boolean)));
        if (ids.length) {
          const results = await Promise.all(
            ids.map(async (id) => {
              try {
                const fb = await getEventFeedback(id); // { event_id, my, positive, negative }
                return [id, fb];
              } catch {
                return [id, { my: null, positive: 0, negative: 0 }];
              }
            })
          );
          if (!mounted) return;
          setFeedbackByEvent(Object.fromEntries(results.map(([id, fb]) => [id, fb])));
        } else {
          setFeedbackByEvent({});
        }
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
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

      {/* Likes / Dislikes for the event */}
      <div style={{ marginTop: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <FaThumbsUp
              title="Лайк мероприятию"
              style={{
                cursor: "pointer",
                color: feedbackByEvent[b.event_id]?.my === "positive" ? "#10b981" : "#9ca3af",
                fontSize: 20,
              }}
              onClick={(e) => {
                e.stopPropagation();
                handleEventFeedback(b.event_id, "positive");
              }}
            />
            <span style={{ fontSize: 13, color: "#374151" }}>
              {feedbackByEvent[b.event_id]?.positive ?? 0}
            </span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <FaThumbsDown
              title="Дизлайк мероприятию"
              style={{
                cursor: "pointer",
                color: feedbackByEvent[b.event_id]?.my === "negative" ? "#ef4444" : "#9ca3af",
                fontSize: 20,
              }}
              onClick={(e) => {
                e.stopPropagation();
                handleEventFeedback(b.event_id, "negative");
              }}
            />
            <span style={{ fontSize: 13, color: "#374151" }}>
              {feedbackByEvent[b.event_id]?.negative ?? 0}
            </span>
          </div>
        </div>
      </div>

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