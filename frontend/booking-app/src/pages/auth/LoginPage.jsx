// src/pages/auth/LoginPage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import styles from "./LoginPage.module.css";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post("/api/v1/auth/login", { email, password });
      localStorage.setItem("access_token", res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);
      navigate("/");
    } catch (e) {
      alert("Ошибка авторизации");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.form}>
        <h2>Вход</h2>
        <input
          className={styles.input}
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          className={styles.input}
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Пароль"
        />
        <button className={styles.button} onClick={handleLogin}>
          Войти
        </button>
        <button
          className={styles.button}
          onClick={() => navigate("/register")}
          style={{ marginTop: "10px", backgroundColor: "#6c757d" }}
        >
          Регистрация
        </button>
      </div>
    </div>
  );
}

// Пример запроса с авторизацией:
// axios.get('/api/v1/some-endpoint', { headers: getAuthHeaders() })
