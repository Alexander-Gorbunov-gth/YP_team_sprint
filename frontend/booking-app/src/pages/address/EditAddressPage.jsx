import { suggestAddress } from "../../api/dadataApi";
import { updateAddress, getMyAddresses, deleteAddress } from "../../api/addressApi";
import { useNavigate, useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import styles from "./EditAddressPage.module.css";
import { parseDadataAddress } from "../../services/dadataParser";


export default function EditAddressPage() {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selected, setSelected] = useState(null);
  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    getMyAddresses().then((addresses) => {
      const existing = addresses.find((addr) => addr.id === id);
      if (existing) {
        setQuery(`${existing.country}, ${existing.city}, ${existing.street}, ${existing.house}`);
      }
    });
  }, [id]);

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      if (query.length > 2) {
        suggestAddress(query).then(setSuggestions);
      } else {
        setSuggestions([]);
      }
    }, 300);
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
    console.log("Данные для Patch:", addressData);
    updateAddress(id, addressData)
      .then(() => {
        navigate("/addresses/new");
      })
      .catch((err) => {
        console.error("Ошибка при обновлении адреса", err);
        alert("Не удалось сохранить адрес");
      });
  };



  return (
    <div className={styles.container}>
      <h2>Редактировать адрес</h2>
      <input
        type="text"
        placeholder="Введите адрес"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className={styles.input}
      />
      {suggestions.length > 0 && (
        <ul className={styles.suggestionsList}>
          {suggestions.map((sugg, index) => (
            <li
              key={index}
              onClick={() => handleSelect(sugg)}
              className={styles.suggestionItem}
            >
              {sugg.value}
            </li>
          ))}
        </ul>
      )}
       <button className={styles.saveButton} onClick={handleSave}>
        Сохранить адрес
      </button>
     
     
    </div>
  );
}