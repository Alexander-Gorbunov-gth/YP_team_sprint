import styles from './Sidebar.module.css';
import { Link } from "react-router-dom";
import { useEffect, useState } from 'react';
import { getUserFeedback, getUserEventsFeedback } from "../../api/userFeedbackApi";
import { getMyProfile } from "../../api/authApi";

export default function Sidebar() {
  const [username, setUsername] = useState(localStorage.getItem('username'));
  const [userId, setUserId] = useState(localStorage.getItem('user_id'));
  const [eventsFeedback, setEventsFeedback] = useState({ positive: 0, negative: 0 });
  const [myFeedback, setMyFeedback] = useState({ positive: 0, negative: 0 });

  const initial = (username?.[0] || '').toUpperCase();

  useEffect(() => {
    if (!username) {
      (async () => {
        try {
          const data = await getMyProfile();
          console.log(data)
          if (data && data.username) {
            setUsername(data.username);
            localStorage.setItem('username', data.username);
          }
          if (data && data.id) {
            setUserId(data.id);
            localStorage.setItem('user_id', data.id);
          }
        } catch (error) {
          // Optionally handle errors here (e.g., log or ignore)
        }
      })();
    }
  }, [username]);

  useEffect(() => {
    let isMounted = true;
    (async () => {
      if (!userId) return;
      try {
        const ef = await getUserEventsFeedback(userId);
        if (isMounted && ef) {
          setEventsFeedback({
            positive: Number(ef.positive ?? 0),
            negative: Number(ef.negative ?? 0),
          });
        }
      } catch (_) {
        // ignore errors
      }
    })();
    return () => { isMounted = false; };
  }, [userId]);

  useEffect(() => {
    let isMounted = true;
    (async () => {
      if (!userId) return;
      try {
        const uf = await getUserFeedback(userId);
        if (isMounted && uf) {
          setMyFeedback({
            positive: Number(uf.positive ?? 0),
            negative: Number(uf.negative ?? 0),
          });
        }
      } catch (_) {
        // ignore errors
      }
    })();
    return () => { isMounted = false; };
  }, [userId]);

  return (
    <aside className={styles.sidebar}>
      <h2 className={styles.title}>Меню</h2>
      
      <Link className={styles.link} to="/events">События</Link>
      <Link className={styles.link} to="/my-events">Мои события</Link>
      <Link className={styles.link} to="/bookings">Бронирования</Link>
      <Link className={styles.link} to="/subscriptions">Подписки</Link>
      {/* <Link className={styles.link} to="/notifications">Уведомления</Link> */}
      <div className={styles.profileCard}>
        <div className={styles.profileHeader}>
          <div className={styles.avatar}>{initial || '👤'}</div>
          <div className={styles.profileText}>
            <div className={styles.welcome}>Вы вошли как</div>
            <div className={styles.name}>{username || '—'}</div>
          </div>
        </div>
        <div className={styles.divider}></div>
        <div className={styles.stats}>
          <div className={styles.statItem} title="Мои оценки (лаики/дизлайки)">
            <span className={styles.statIcon}>👤</span>
            <div className={styles.statNumbers}>
              <span className={styles.statValue}>👍 {myFeedback.positive}</span>
              <span className={styles.statValueMuted}> / 👎 {myFeedback.negative}</span>
            </div>
            <div className={styles.statLabel}>Мои оценки</div>
          </div>
          <div className={styles.statItem} title="Оценки моих событий">
            <span className={styles.statIcon}>🎬</span>
            <div className={styles.statNumbers}>
              <span className={styles.statValue}>👍 {eventsFeedback.positive}</span>
              <span className={styles.statValueMuted}> / 👎 {eventsFeedback.negative}</span>
            </div>
            <div className={styles.statLabel}>Мои события</div>
          </div>
        </div>
      </div>
      <button className={styles.logoutBtn} onClick={() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
        localStorage.removeItem('user_id');
        window.location.href = '/';
      }}>
        Выйти
      </button>
    </aside>
  );
}