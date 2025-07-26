import { useEffect, useState } from "react";
import { getMySubscriptions, deleteSubscription } from "../../api/subscriptionApi";
import styles from "./SubscriptionsPage.module.css";

export default function SubscriptionsPage() {
  const [subscriptions, setSubscriptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMySubscriptions()
      .then((data) => {
        setSubscriptions(data || []);
      })
      .finally(() => setLoading(false));
  }, []);

  const handleUnsubscribe = async (host_id) => {
    try {
      await deleteSubscription(host_id);
      setSubscriptions((prev) => prev.filter((s) => s.host_id !== host_id));
    } catch (error) {
      alert("Не удалось отменить подписку");
    }
  };

  if (loading) return <p>Загрузка...</p>;
  if (!subscriptions.length) return <p>Подписок пока нет</p>;

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Мои подписки</h2>
      <div className={styles.grid}>
        {subscriptions.map((sub) => (
          <div key={sub.host_id} className={styles.card}>
            <p><strong>Имя:</strong> {sub.author.name}</p>
            <p><strong>Username:</strong> {sub.author.username}</p>
            <button
              className={styles.unsubscribeButton}
              onClick={() => handleUnsubscribe(sub.host_id)}
            >
              Отменить подписку
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}