import { suggestAddress } from "../../api/dadataApi";
import { createAddress, getMyAddresses, deleteAddress } from "../../api/addressApi";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./AddAddressPage.module.css";
import { parseDadataAddress } from "../../services/dadataParser";


export default function AddAddressPage() {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selected, setSelected] = useState(null);
  const [myAddresses, setMyAddresses] = useState([]);
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

  useEffect(() => {
    getMyAddresses()
      .then(setMyAddresses)
      .catch((err) => {
        console.error("Ошибка при получении адресов", err);
      });
  }, []);

  const handleSelect = (sugg) => {
    setSelected(sugg);
    setQuery(sugg.value);
    setSuggestions([]);
  };

  const handleSave = () => {
    if (!selected) return;
    console.log(selected.data)
    const addressData = parseDadataAddress(selected.data);
    // console.log("Данные для POST:", addressData);
    createAddress(addressData)
      .then(() => {
        navigate("/my-events");
      })
      .catch((err) => {
        console.error("Ошибка при создании адреса", err);
        alert("Не удалось сохранить адрес");
      });
  };

  const handleDelete = async (id) => {
    try {
      await deleteAddress(id);
      setMyAddresses((prev) => prev.filter((a) => a.id !== id));
    } catch (err) {
      console.error("Ошибка при удалении адреса", err);
      alert("Не удалось удалить адрес");
    }
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
       <button className={styles.saveButton} onClick={handleSave}>
        Сохранить адрес
      </button>
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
      {myAddresses.length > 0 && (
        <div className={styles.myAddresses}>
          <h3>Мои адреса</h3>
          <ul>
            {myAddresses.map((addr) => (
              <li key={addr.id} className={styles.addressItem}>
                <div>
                  {addr.country}, {addr.city}, {addr.street} {addr.house}
                  {addr.flat ? `, кв. ${addr.flat}` : ""}
                </div>
                <div className={styles.buttonGroup}>
                  <button
                    onClick={() => navigate(`/edit-address/${addr.id}`)}
                    className={styles.iconButton}
                    aria-label="Изменить"
                  >
                    <i className="bi bi-pencil"></i>
                  </button>
                  <button
                    onClick={() => handleDelete(addr.id)}
                    className={styles.iconButton}
                    aria-label="Удалить"
                  >
                    <i className="bi bi-trash"></i>
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
     
    </div>
  );
}