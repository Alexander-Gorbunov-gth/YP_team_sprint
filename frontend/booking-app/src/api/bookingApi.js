


export async function createReservation(payload) {
  const res = await axios.post(`${API_BASE}/reservations`, payload);
  return res.data;
}