import { useState } from "react";

function UploadCSV() {
  const [fileName, setFileName] = useState(null);

  const handleChange = (event) => {
    const file = event.target.files?.[0];
    setFileName(file ? file.name : null);
  };

  return (
    <section className="card">
      <h2>Importer un CSV</h2>
      <input type="file" accept=".csv" onChange={handleChange} />
      {fileName && <p>Fichier sélectionné : {fileName}</p>}
    </section>
  );
}

export default UploadCSV;
