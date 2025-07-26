import axios from "axios";

const DADATA_API_KEY = import.meta.env.VITE_DADATA_API_KEY;
const DADATA_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address";

export async function suggestAddress(query) {
  const response = await axios.post(
    DADATA_URL,
    { query },
    {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${DADATA_API_KEY}`,
      },
    }
  );
  
  return response.data.suggestions; // массив адресов
}