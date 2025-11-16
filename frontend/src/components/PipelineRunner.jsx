import { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:18000";

export default function PipelineRunner({ filePath, onResult }) {
  const [isRunning, setIsRunning] = useState(false);
  const [message, setMessage] = useState(null);

  const run = async () => {
    if (!filePath) return;
    setIsRunning(true);
    setMessage(null);
    try {
      const { data } = await axios.post(`${API_URL}/run`, {
        file_path: filePath
      });
      setMessage("Pipeline exécutée avec succès ✅");
      onResult?.(data);
    } catch (error) {
      console.error(error);
      setMessage("Échec du lancement de la pipeline ❌");
    } finally {
      setIsRunning(false);
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
    </section>
  );
}
