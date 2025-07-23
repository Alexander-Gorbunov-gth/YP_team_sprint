import styles from './Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>Сервис бронирования</h1>
    </header>
  );
}