import { useEffect, useState } from "react";
import axios from "axios";
import { API_URL } from "../config";

export default function HistoryViewer({ refreshKey = 0 }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const { data } = await axios.get(`${API_URL}/history`);
        setHistory(data.records || []);
      } catch (error) {
        console.error("Unable to load history", error);
      }
    }
    fetchHistory();
  }, [refreshKey]);

  return (
    <section className="card">
      <h2>Historique global</h2>
      {history.length === 0 ? (
        <p>Aucun historique disponible.</p>
      ) : (
        <ul className="history-list">
          {history.slice(0, 10).map((item, index) => (
            <li key={`${item.CIP || index}-${index}`}>
              <strong>{item.Libelle || "Libellé inconnu"}</strong> —
              {item.Univers || "Univers ?"} / {item.Famille || "Famille ?"}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
