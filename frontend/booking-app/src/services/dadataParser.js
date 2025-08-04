
export function parseDadataAddress(data) {
  return {
    country: data.country || "Россия",
    latitude: data.geo_lat || undefined,
    longitude: data.geo_lon || undefined,
    city: data.city || "",
    street: data.street_with_type || "",
    house: data.house || "",
    flat: data.flat || undefined,
  };
}