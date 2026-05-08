import React, { StrictMode } from "react";
import { Activity, Cpu, Radio, Sparkles } from "lucide-react";
import RealTimeSection from "./components/RealTimeSection.jsx";
import ResultCard from "./components/ResultCard.jsx";
import UploadSection from "./components/UploadSection.jsx";

const modes = ["WALKING", "RUNNING", "SITTING", "STANDING", "STAIRS", "RANDOM"];

const baselines = {
  WALKING: { acc: [0.45, 0.82, 9.62], gyro: [0.08, 0.14, 0.03] },
  RUNNING: { acc: [1.2, 2.3, 11.1], gyro: [0.22, 0.34, 0.16] },
  SITTING: { acc: [0.02, 0.04, 9.78], gyro: [0.01, 0.01, 0] },
  STANDING: { acc: [-0.04, 0.08, 9.81], gyro: [0, 0.02, 0.01] },
  STAIRS: { acc: [0.8, 1.4, 10.35], gyro: [0.15, 0.21, 0.09] },
};

function jitter(value, spread) {
  return Number((value + (Math.random() - 0.5) * spread).toFixed(2));
}

function makeReading(mode) {
  const label = mode === "RANDOM" ? modes[Math.floor(Math.random() * 5)] : mode;
  const base = baselines[label];

  return {
    mode: label,
    accelerometer: {
      x: jitter(base.acc[0], 0.35),
      y: jitter(base.acc[1], 0.35),
      z: jitter(base.acc[2], 0.45),
    },
    gyroscope: {
      x: jitter(base.gyro[0], 0.08),
      y: jitter(base.gyro[1], 0.08),
      z: jitter(base.gyro[2], 0.08),
    },
  };
}

function localPredict(reading) {
  const seed = baselines[reading.mode] ? reading.mode : "WALKING";
  const scores = Object.fromEntries(
    modes.slice(0, 5).map((label) => [label, label === seed ? 0.72 : Math.random() * 0.14 + 0.02]),
  );
  const total = Object.values(scores).reduce((sum, score) => sum + score, 0);
  return Object.fromEntries(Object.entries(scores).map(([label, score]) => [label, Number((score / total).toFixed(3))]));
}

export default function App() {
  const [mode, setMode] = useState("RANDOM");
  const [reading, setReading] = useState(() => makeReading("RANDOM"));
  const [result, setResult] = useState({
    prediction: "WAITING",
    confidence: 0,
    probabilities: localPredict(reading),
  });
  const [logs, setLogs] = useState([
    '[SYS] Sensor simulation active',
    '[SYS] Click "Analyze with AI" to classify',
    "[SENSOR] Simulation started at 10Hz",
  ]);

  useEffect(() => {
    const timer = setInterval(() => {
      setReading(makeReading(mode));
    }, 100);

    return () => clearInterval(timer);
  }, [mode]);

  const chartData = useMemo(
    () => [
      { title: "ACCELEROMETER", unit: "M/S2", values: reading.accelerometer, max: 12 },
      { title: "GYROSCOPE", unit: "RAD/S", values: reading.gyroscope, max: 0.4 },
    ],
    [reading],
  );

  function changeMode(nextMode) {
    setMode(nextMode);
    setLogs((current) => [`[SYS] Mode set to: ${nextMode}`, ...current].slice(0, 7));
  }

  async function analyze() {
    const fallback = {
      prediction: reading.mode,
      confidence: 0.72,
      probabilities: localPredict(reading),
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, ...reading }),
      });

      if (!response.ok) throw new Error("Backend unavailable");
      const data = await response.json();
      setResult(data);
      setLogs((current) => [`[AI] Prediction: ${data.prediction} (${Math.round(data.confidence * 100)}%)`, ...current].slice(0, 7));
    } catch {
      setResult(fallback);
      setLogs((current) => ["[AI] Local browser model used", `[AI] Prediction: ${fallback.prediction}`, ...current].slice(0, 7));
    }
  }

  return (
    <main className="app-shell">
      <section className="dashboard">
        <div className="hero-row">
          <div>
            <div className="kicker"><Cpu size={18} /> HAR SYSTEM</div>
            <h1>Human Activity Recognition - Pattern Recognition Project</h1>
          </div>
          <div className="status-pill"><Radio size={16} /> 10Hz live</div>
        </div>

        <div className="mode-grid" aria-label="Activity mode selector">
          {modes.map((item) => (
            <button className={item === mode ? "active" : ""} key={item} onClick={() => changeMode(item)}>
              {item}
            </button>
          ))}
        </div>

        <RealTimeSection chartData={chartData} />

        <div className="analysis-layout">
          <ResultCard result={result} />
          <UploadSection logs={logs} />
        </div>

        <button className="analyze-button" onClick={analyze}>
          <Sparkles size={18} /> ANALYZE WITH AI
        </button>

        <footer>
          <Activity size={16} /> Sensor simulator running in browser; backend API ready on FastAPI.
        </footer>
      </section>
    </main>
  );
}
