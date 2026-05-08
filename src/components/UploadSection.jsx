import React from "react";

export default function UploadSection({ logs }) {
  return (
    <section className="log-panel">
      <h2>SYSTEM LOG</h2>
      <div className="terminal">
        {logs.map((line, index) => (
          <p key={`${line}-${index}`}>{line}</p>
        ))}
      </div>
    </section>
  );
}
