import styles from './Sidebar.module.css';
import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <h2 className={styles.title}>Меню</h2>
      <Link className={styles.link} to="/events">События</Link>
      <Link className={styles.link} to="/my-events">Мои события</Link>
      <Link className={styles.link} to="/bookings">Бронирования</Link>
      <Link className={styles.link} to="/subscriptions">Подписки</Link>
      {/* <Link className={styles.link} to="/notifications">Уведомления</Link> */}
    </aside>
  );
}