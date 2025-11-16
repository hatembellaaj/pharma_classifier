import { useEffect, useState } from "react";
import axios from "axios";
import { API_URL } from "../config";

export default function HistoryViewer({ refreshKey = 0 }) {
  const [isLoading, setIsLoading] = useState(true);
  const [lineCount, setLineCount] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchHistory() {
      setIsLoading(true);
      setError(null);
      try {
        const { data } = await axios.get(`${API_URL}/history`);
        if (!isMounted) return;
        const records = data.records || [];
        setLineCount(records.length);
      } catch (fetchError) {
        if (!isMounted) return;
        console.error("Unable to load history", fetchError);
        setError(
          "Impossible de charger l'historique pour le moment. Merci de réessayer."
        );
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchHistory();

    return () => {
      isMounted = false;
    };
  }, [refreshKey]);

  return (
    <section className="card">
      <h2>Historique global</h2>
      {isLoading ? (
        <div className="loading-state" aria-busy="true">
          <span className="loading-spinner" aria-hidden="true" />
          <p>Chargement de l'historique, merci de patienter…</p>
        </div>
      ) : error ? (
        <p role="alert" className="subtitle">
          {error}
        </p>
      ) : lineCount === 0 ? (
        <p className="subtitle">Aucun historique disponible.</p>
      ) : (
        <p className="subtitle">
          Historique chargé · {lineCount} lignes disponibles dans votre fichier.
        </p>
      )}
    </section>
  );
}
