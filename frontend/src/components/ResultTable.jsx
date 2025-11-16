import { useState } from "react";

const sampleResults = [
  { id: "1", texte: "Doliprane 500mg", categorie: "antalgique" },
  { id: "2", texte: "Sirop contre la toux", categorie: "toux" }
];

function ResultTable() {
  const [results] = useState(sampleResults);

  return (
    <section className="card">
      <h2>Résultats</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Description</th>
            <th>Catégorie</th>
          </tr>
        </thead>
        <tbody>
          {results.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.texte}</td>
              <td>{row.categorie}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export default ResultTable;
