import { suggestAddress } from "../../api/dadataApi";
import { useState, useEffect } from "react";
import styles from "./AddAddressPage.module.css";

export default function AddAddressPage() {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selected, setSelected] = useState(null);

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
    console.log("Выбранный адрес:", sugg);
    setQuery(sugg.value);
    setSuggestions([]);
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
      <button className={styles.saveButton}>
        Сохранить адрес
      </button>
    </div>
  );
}