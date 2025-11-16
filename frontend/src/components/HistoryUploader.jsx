import { useState } from "react";
import axios from "axios";
import { API_URL } from "../config";

export default function HistoryUploader({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const upload = async () => {
    if (!file) return;
    setIsUploading(true);
    setStatus("Envoi de l'historique...");
    const form = new FormData();
    form.append("file", file);
    try {
      await axios.post(`${API_URL}/history/upload`, form);
      setStatus("Historique mis à jour ✔️");
      setFile(null);
      onUploaded?.();
    } catch (error) {
      console.error("Unable to upload history", error);
      setStatus("Échec de l'import de l'historique ❌");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <section className="card">
      <h2>Mettre à jour l'historique</h2>
      <p className="subtitle">Importe le dernier fichier d'historique global.</p>
      <input
        type="file"
        accept=".csv"
        onChange={(event) => {
          const selected = event.target.files?.[0];
          setFile(selected || null);
          setStatus(null);
        }}
      />
      <button onClick={upload} disabled={!file || isUploading}>
        {isUploading ? "Chargement..." : "Charger l'historique"}
      </button>
      {file && <p>Fichier sélectionné : {file.name}</p>}
      {status && <p className="status">{status}</p>}
    </section>
  );
}
