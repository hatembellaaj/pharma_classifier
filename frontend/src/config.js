const FALLBACK_URL = "http://localhost:18000";

const getDefaultApiUrl = () => {
  if (typeof window === "undefined") {
    return FALLBACK_URL;
  }
  const { protocol, hostname } = window.location;
  return `${protocol}//${hostname}:18000`;
};

export const API_URL = (import.meta.env.VITE_API_URL || "").trim() || getDefaultApiUrl();
