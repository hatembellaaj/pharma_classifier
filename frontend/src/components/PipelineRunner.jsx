import { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function PipelineRunner() {
  const [isRunning, setIsRunning] = useState(false);
  const [message, setMessage] = useState(null);

  const handleRun = async () => {
    setIsRunning(true);
    setMessage(null);
    try {
      await axios.post(`${API_URL}/pipeline/run`);
      setMessage("Pipeline lancée avec succès");
    } catch (error) {
      setMessage("Échec du lancement de la pipeline");
      console.error(error);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <section className="card">
      <h2>Pipeline</h2>
      <button onClick={handleRun} disabled={isRunning}>
        {isRunning ? "En cours..." : "Lancer"}
      </button>
      {message && <p>{message}</p>}
    </section>
  );
}

export default PipelineRunner;
