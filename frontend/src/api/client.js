import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 150000, // generous timeout; generation can take a while on free tiers
});

/**
 * Extract a human-readable error message from any Axios error shape,
 * covering network failures, timeouts, and structured backend error bodies.
 */
export function extractErrorMessage(error) {
  if (error.code === "ECONNABORTED") {
    return "Video generation is taking too long. Please try again.";
  }
  if (!error.response) {
    return "Network error — please check your connection and that the backend is running.";
  }
  const data = error.response.data;
  if (data?.detail) {
    return data.detail;
  }
  return "Something went wrong. Please try again.";
}

export async function generateVideo(prompt) {
  const { data } = await apiClient.post("/generate", { prompt });
  return data;
}

export async function fetchHistory() {
  const { data } = await apiClient.get("/history");
  return data;
}

export async function deleteHistoryItem(id) {
  await apiClient.delete(`/history/${id}`);
}
