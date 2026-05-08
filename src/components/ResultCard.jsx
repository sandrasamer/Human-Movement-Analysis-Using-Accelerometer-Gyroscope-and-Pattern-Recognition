import React from "react";

export default function ResultCard({ result }) {
  const probabilities = result.probabilities || {};

  return (
    <section className="result-panel">
      <h2>ACTIVITY PROBABILITIES</h2>
      <div className="prediction">
        <span>Prediction</span>
        <strong>{result.prediction}</strong>
      </div>
      {result.model_type && <p className="model-note">Using {result.model_type}</p>}
      {Object.entries(probabilities).map(([label, score]) => (
        <div className="probability-row" key={label}>
          <span>{label}</span>
          <div className="probability-track">
            <div style={{ width: `${Math.round(score * 100)}%` }} />
          </div>
          <b>{Math.round(score * 100)}%</b>
        </div>
      ))}
    </section>
  );
}
