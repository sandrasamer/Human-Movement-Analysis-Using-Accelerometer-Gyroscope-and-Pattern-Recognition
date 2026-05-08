import React from "react";

const axes = ["x", "y", "z"];

export default function RealTimeSection({ chartData }) {
  return (
    <section className="sensor-grid">
      {chartData.map((group) => (
        <article className="sensor-panel" key={group.title}>
          <h2><span /> {group.title} ({group.unit})</h2>
          {axes.map((axis) => {
            const value = group.values[axis];
            const percent = Math.min(100, Math.abs(value / group.max) * 100);

            return (
              <div className="axis-row" key={axis}>
                <div className="axis-label">{axis.toUpperCase()}</div>
                <div className="meter">
                  <div style={{ width: `${percent}%` }} />
                </div>
                <strong>{value.toFixed(2)}</strong>
              </div>
            );
          })}
        </article>
      ))}
    </section>
  );
}
