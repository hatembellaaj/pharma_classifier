import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function HistoryViewer() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const { data } = await axios.get(`${API_URL}/history`);
        setHistory(data.records ?? []);
      } catch (error) {
        console.error("Unable to load history", error);
      }
    }
    fetchHistory();
  }, []);

  return (
    <section className="card">
      <h2>Historique</h2>
      {history.length === 0 ? (
        <p>Aucun historique disponible.</p>
      ) : (
        <ul>
          {history.map((item) => (
            <li key={item.id}>
              #{item.id} — {item.categorie}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default HistoryViewer;
