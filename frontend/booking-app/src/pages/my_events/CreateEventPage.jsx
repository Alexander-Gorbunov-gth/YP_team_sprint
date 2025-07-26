import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createEvent } from "../../api/eventApi";
import { getMyAddresses } from "../../api/addressApi";
import styles from "./CreateEventPage.module.css";
import { searchFilms } from '../../api/filmApi';


export default function CreateEventPage({ movies = [] }) {
  const [movieId, setMovieId] = useState("");
  const [addressId, setAddressId] = useState("");
  const [capacity, setCapacity] = useState(10);
  const [startDatetime, setStartDatetime] = useState("");
  const [addresses, setAddresses] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getMyAddresses().then((data) => setAddresses(data || []));
  }, []);

  useEffect(() => {
  const delayDebounce = setTimeout(() => {
    if (searchQuery.length > 1) {
      searchFilms(searchQuery)
        .then(setSearchResults)
        .catch(() => setSearchResults([]));
    } else {
      setSearchResults([]);
    }
  }, 1);
  return () => clearTimeout(delayDebounce);
}, [searchQuery]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try { 
      await createEvent({
        movie_id: movieId,
        address_id: addressId,
        capacity: Number(capacity),
        start_datetime: new Date(startDatetime).toISOString(),
      });
      navigate("/my-events");
    } catch (error) {
      alert("Ошибка при создании мероприятия");
    }
  };

  return (
    <div className={styles.container}>
      <p className={styles.title}>Создать мероприятие</p>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formRow}>
          <label className={styles.label} style={{ position: "relative" }}>
            Фильм:
            <input
              type="text"
              className={styles.input}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Введите название фильма"
            />
            {searchQuery.length > 1 && (
              <ul className={styles.dropdown}>
                {searchResults.length > 0 ? (
                  searchResults.map((movie) => (
                    <li
                      key={movie.id}
                      className={styles.dropdownItem}
                      onClick={() => {
                        setMovieId(movie.id);
                        setSearchQuery(movie.title);
                        setSearchResults([]);
                      }}
                    >
                      {movie.title}
                    </li>
                  ))
                ) : (
                  <li className={styles.dropdownItem}>Фильмы не найдены</li>
                )}
              </ul>
            )}
          </label>

          <label className={styles.label}>
            Адрес:
            <select
              className={styles.input}
              value={addressId}
              onChange={(e) => setAddressId(e.target.value)}
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
              value={capacity}
              onChange={(e) => setCapacity(e.target.value)}
              required
              min="1"
              className={styles.input}
            />
          </label>

          <label className={styles.label}>
            Дата и время:
            <input
              type="datetime-local"
              value={startDatetime}
              onChange={(e) => setStartDatetime(e.target.value)}
              required
              className={styles.input}
            />
          </label>
        </div>

        <button type="submit" className={styles.button}>
          Создать
        </button>
        {/* <button
          type="button"
          className={styles.secondaryButton}
          onClick={() => navigate("/addresses/new")}
        >
          ➕ Добавить адрес
        </button> */}
      </form>
    </div>
  );
}