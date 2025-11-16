import { useState } from "react";
import UploadCSV from "./components/UploadCSV";
import PipelineRunner from "./components/PipelineRunner";
import ResultTable from "./components/ResultTable";
import HistoryViewer from "./components/HistoryViewer";
import HistoryUploader from "./components/HistoryUploader";
import axios from "axios";
import Papa from "papaparse";
import "./styles.css";
import { API_URL } from "./config";

function App() {
  const [filePath, setFilePath] = useState(null);
  const [resultMeta, setResultMeta] = useState(null);
  const [rows, setRows] = useState([]);
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

  const refreshResults = async () => {
    try {
      const { data } = await axios.get(`${API_URL}/results`);
      setRows(data.records || []);
    } catch (error) {
      console.error("Unable to load structured results", error);
      try {
        const response = await axios.get(`${API_URL}/download`, { responseType: "blob" });
        const text = await response.data.text();
        const parsed = Papa.parse(text, { header: true });
        const filtered = (parsed.data || []).filter((row) =>
          Object.values(row || {}).some((value) => value && `${value}`.trim().length > 0)
        );
        setRows(filtered);
      } catch (fallbackError) {
        console.error("Unable to load CSV results", fallbackError);
      }
    }
  };

  const refreshHistory = () => setHistoryRefreshKey((prev) => prev + 1);

  return (
    <div className="app">
      <header>
        <div>
          <p className="eyebrow">Suite métier</p>
          <h1>Pharma Classifier</h1>
          <p className="subtitle">
            Upload, lance et visualise la classification médicaments / parapharmacie.
          </p>
        </div>
      </header>

      <UploadCSV
        onUploaded={(path) => {
          setFilePath(path);
          setResultMeta(null);
          setRows([]);
        }}
      />
      <PipelineRunner
        filePath={filePath}
        onResult={(meta) => {
          setResultMeta(meta);
          refreshResults();
          refreshHistory();
        }}
      />

      {resultMeta && (
        <section className="card stats">
          <div>
            <span>Fichier traité</span>
            <strong>{resultMeta.output}</strong>
          </div>
          <div>
            <span>Lignes classifiées</span>
            <strong>{resultMeta.rows}</strong>
          </div>
        </section>
      )}

      {rows.length > 0 && <ResultTable rows={rows} />}

      <HistoryUploader onUploaded={refreshHistory} />

      <HistoryViewer refreshKey={historyRefreshKey} />
    </div>
  );
}

export default App;
