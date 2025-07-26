
export function parseDadataAddress(data) {
  return {
    country: data.country || "Россия",
    city: data.city || "",
    street: data.street_with_type || "",
    house: data.house || "",
    flat: data.flat || undefined,
  };
}