import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api/v1";

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("civic_access_token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refresh = localStorage.getItem("civic_refresh_token");
      if (refresh) {
        try {
          const res = await axios.post(`${API_BASE}/auth/token/refresh/`, { refresh });
          const newAccess = res.data.access;
          localStorage.setItem("civic_access_token", newAccess);
          originalRequest.headers.Authorization = `Bearer ${newAccess}`;
          return apiClient(originalRequest);
        } catch (refreshErr) {
          localStorage.removeItem("civic_access_token");
          localStorage.removeItem("civic_refresh_token");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);
