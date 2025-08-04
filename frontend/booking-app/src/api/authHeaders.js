

export const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token");
  console.log("Токен авторизации:", token);
  return token ? { Authorization: `Bearer ${token}` } : {};
};