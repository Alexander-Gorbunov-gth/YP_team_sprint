import { suggestAddress } from "../../api/dadataApi";
import { createAddress } from "../../api/addressApi";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./AddAddressPage.module.css";
import { parseDadataAddress } from "../../services/dadataParser";


export default function AddAddressPage() {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selected, setSelected] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      if (query.length > 2) {
        suggestAddress(query).then(setSuggestions);
      } else {
        setSuggestions([]);
      }
    }, 1);
    return () => clearTimeout(delayDebounce);
  }, [query]);

  const handleSelect = (sugg) => {
    setSelected(sugg);
    setQuery(sugg.value);
    setSuggestions([]);
  };

  const handleSave = () => {
    if (!selected) return;
    const addressData = parseDadataAddress(selected.data);
    console.log("Данные для POST:", addressData);
    createAddress(addressData)
      .then(() => {
        navigate("/my-events");
      })
      .catch((err) => {
        console.error("Ошибка при создании адреса", err);
        alert("Не удалось сохранить адрес");
      });
  };

  return (
    <div className={styles.container}>
      <h2>Добавить адрес</h2>
      <input
        type="text"
        placeholder="Введите адрес"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className={styles.input}
      />
      {suggestions.length > 0 && (
        <div className={styles.suggestionsList}>
          {suggestions.map((s, idx) => (
            <div
              key={idx}
              onClick={() => handleSelect(s)}
              className={styles.suggestionItem}
            >
              {s.value}
            </div>
          ))}
        </div>
      )}
      {selected && (
        <div className={styles.selectedInfo}>
          <p><strong>Город:</strong> {selected.data.city}</p>
          <p><strong>Улица:</strong> {selected.data.street_with_type}</p>
          <p><strong>Дом:</strong> {selected.data.house}</p>
        </div>
      )}
      <button className={styles.saveButton} onClick={handleSave}>
        Сохранить адрес
      </button>
    </div>
  );
}