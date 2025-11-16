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

  const preferredColumns = [
    "CIP",
    "Libelle",
    "Marque",
    "Univers",
    "Famille",
    "Tablette",
    "Tablette_consolidee",
  ];
  const discoveredColumns =
    history.length > 0 ? Object.keys(history[0]) : preferredColumns;
  const orderedColumns = [
    ...preferredColumns.filter((column) => discoveredColumns.includes(column)),
    ...discoveredColumns.filter((column) => !preferredColumns.includes(column)),
  ];

  return (
    <section className="card">
      <h2>Historique global</h2>
      {history.length === 0 ? (
        <p>Aucun historique disponible.</p>
      ) : (
        <>
          <p className="subtitle">
            {history.length} lignes importées · Les colonnes sont affichées comme dans
            le CSV fourni
          </p>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  {orderedColumns.map((column) => (
                    <th key={column}>{column}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {history.map((row, index) => (
                  <tr key={`${row.CIP || row.Libelle || index}-${index}`}>
                    {orderedColumns.map((column) => (
                      <td key={`${column}-${index}`}>{row[column] || "-"}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  );
}
