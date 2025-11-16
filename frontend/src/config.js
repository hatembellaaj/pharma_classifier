const LOCAL_HOSTS = new Set(["localhost", "127.0.0.1"]);

const PORT_MAPPING = {
  // Local Vite dev server → local FastAPI default port
  "5173": "8000",
  // Docker compose (UI exposed on 18100 → API on 18000)
  "18100": "18000",
};

const buildUrl = (protocol, hostname, port) => `${protocol}//${hostname}:${port}`;

const getFallbackUrl = ({ protocol, hostname }) => {
  if (LOCAL_HOSTS.has(hostname)) {
    return buildUrl(protocol, hostname, "8000");
  }

  return buildUrl(protocol, hostname, "18000");
};

const getDefaultApiUrl = () => {
  if (typeof window === "undefined") {
    return "http://localhost:8000";
  }

  const { protocol, hostname, port } = window.location;
  const targetPort = PORT_MAPPING[port];

  if (!targetPort) {
    return getFallbackUrl({ protocol, hostname });
  }

  return buildUrl(protocol, hostname, targetPort);
};

export const API_URL = (import.meta.env.VITE_API_URL || "").trim() || getDefaultApiUrl();
