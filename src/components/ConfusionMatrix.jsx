import React from "react";

const shortLabels = {
  WALKING: "Walk",
  RUNNING: "Run",
  SITTING: "Sit",
  STANDING: "Stand",
  STAIRS: "Stairs",
};

export default function ConfusionMatrix({ classes = [], matrix = {} }) {
  const maxValue = Math.max(
    1,
    ...classes.flatMap((actual) => classes.map((predicted) => matrix?.[actual]?.[predicted] || 0)),
  );

  return (
    <section className="matrix-panel">
      <div className="matrix-heading">
        <div>
          <h2>CONFUSION MATRIX</h2>
          <p>Rows are actual activities; columns are predicted activities.</p>
        </div>
        <span>MODEL EVALUATION</span>
      </div>

      <div className="matrix-scroll">
        <div className="matrix-grid" style={{ gridTemplateColumns: `92px repeat(${classes.length}, minmax(72px, 1fr))` }}>
          <div className="matrix-corner">Actual</div>
          {classes.map((label) => (
            <div className="matrix-label" key={`pred-${label}`}>{shortLabels[label] || label}</div>
          ))}

          {classes.map((actual) => (
            <React.Fragment key={actual}>
              <div className="matrix-label row-label">{shortLabels[actual] || actual}</div>
              {classes.map((predicted) => {
                const value = matrix?.[actual]?.[predicted] || 0;
                const strength = value / maxValue;
                const isCorrect = actual === predicted;

                return (
                  <div
                    className={`matrix-cell ${isCorrect ? "correct" : ""}`}
                    key={`${actual}-${predicted}`}
                    style={{ "--strength": strength }}
                    title={`${actual} predicted as ${predicted}: ${value}`}
                  >
                    {value}
                  </div>
                );
              })}
            </React.Fragment>
          ))}
        </div>
      </div>
    </section>
  );
}
