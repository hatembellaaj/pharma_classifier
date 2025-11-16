const FALLBACK_URL = "http://localhost:8000";

const PORT_MAPPING = {
  // Local Vite dev server → local FastAPI default port
  "5173": "8000",
  // Docker compose (UI exposed on 18100 → API on 18000)
  "18100": "18000",
};

const getDefaultApiUrl = () => {
  if (typeof window === "undefined") {
    return FALLBACK_URL;
  }

  const { protocol, hostname, port } = window.location;
  const targetPort = PORT_MAPPING[port];

  if (!targetPort) {
    return FALLBACK_URL;
  }

  return `${protocol}//${hostname}:${targetPort}`;
};

export const API_URL = (import.meta.env.VITE_API_URL || "").trim() || getDefaultApiUrl();
