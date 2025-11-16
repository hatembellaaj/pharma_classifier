import { useRef, useState } from "react";
import axios from "axios";
import { API_URL } from "../config";

export default function PipelineRunner({ filePath, onResult }) {
  const [isRunning, setIsRunning] = useState(false);
  const [message, setMessage] = useState(null);
  const [logs, setLogs] = useState([]);
  const pollingRef = useRef(null);

  const fetchLogs = async () => {
    try {
      const { data } = await axios.get(`${API_URL}/run/logs`);
      setLogs(data.lines || []);
    } catch (error) {
      console.error("Unable to fetch live logs", error);
    }
  };

  const startPolling = () => {
    if (pollingRef.current) return;
    pollingRef.current = setInterval(fetchLogs, 1000);
  };

  const stopPolling = () => {
    if (!pollingRef.current) return;
    clearInterval(pollingRef.current);
    pollingRef.current = null;
  };

  const run = async () => {
    if (!filePath) return;
    setIsRunning(true);
    setMessage(null);
    setLogs([]);
    startPolling();
    try {
      const { data } = await axios.post(`${API_URL}/run`, {
        file_path: filePath
      });
      setMessage("Pipeline exécutée avec succès ✅");
      onResult?.(data);
      setLogs(data.logs || []);
    } catch (error) {
      console.error(error);
      setMessage("Échec du lancement de la pipeline ❌");
    } finally {
      setIsRunning(false);
      stopPolling();
      fetchLogs();
    }
  };

  return (
    <section className="card">
      <h2>Pipeline</h2>
      <button onClick={run} disabled={!filePath || isRunning}>
        {isRunning ? "Exécution..." : "Lancer le pipeline"}
      </button>
      {!filePath && <p className="status">Importe un CSV pour activer le bouton.</p>}
      {message && <p className="status">{message}</p>}
      {logs.length > 0 && (
        <div className="live-logs">
          <p className="status">Journal d'exécution</p>
          <pre>{logs.join("\n")}</pre>
        </div>
      )}
    </section>
  );
}
