import { useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:18000";

export default function UploadCSV({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);

  const upload = async () => {
    if (!file) return;
    setStatus("Envoi en cours...");
    const form = new FormData();
    form.append("file", file);
    try {
      const { data } = await axios.post(`${API_URL}/upload`, form);
      setStatus("Fichier importé avec succès.");
      onUploaded?.(data.path);
    } catch (error) {
      console.error(error);
      setStatus("Erreur lors de l'envoi du fichier.");
    }
  };

  return (
    <section className="card">
      <h2>Uploader un fichier CSV</h2>
      <input
        type="file"
        accept=".csv"
        onChange={(event) => {
          const selected = event.target.files?.[0];
          setFile(selected || null);
          setStatus(null);
        }}
      />
      <button onClick={upload} disabled={!file}>
        Envoyer
      </button>
      {file && <p>Fichier sélectionné : {file.name}</p>}
      {status && <p className="status">{status}</p>}
    </section>
  );
}
