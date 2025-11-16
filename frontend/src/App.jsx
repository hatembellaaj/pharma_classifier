import UploadCSV from "./components/UploadCSV";
import PipelineRunner from "./components/PipelineRunner";
import ResultTable from "./components/ResultTable";
import HistoryViewer from "./components/HistoryViewer";
import "./styles.css";

function App() {
  return (
    <div className="app">
      <h1>Pharma Classifier</h1>
      <UploadCSV />
      <PipelineRunner />
      <ResultTable />
      <HistoryViewer />
    </div>
  );
}

export default App;
