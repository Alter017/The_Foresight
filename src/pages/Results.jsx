import "./Results.css";

import { useLocation } from "react-router-dom";
import { useState } from "react";

function Results() {
  const { state } = useLocation();

  if (!state) {
    return <h2 className="container">No data found</h2>;
  }

  const scenario = state;
  const [customDecision, setCustomDecision] = useState("");

  const handleDecision = async (choice) => {
    const scenarios = JSON.parse(localStorage.getItem("scenarios")) || [];

    const updatedScenario = { ...scenario, finalDecision: choice };

    try {
      const response = await fetch("http://127.0.0.1:5000/scenario/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedScenario),
      });

      if (!response.ok) throw new Error("Failed to save decision");

      const updated = scenarios.map((s) =>
        s.id === scenario.id ? updatedScenario : s
      );
      localStorage.setItem("scenarios", JSON.stringify(updated));

      alert(`Final decision saved: ${choice}`);
    } catch (err) {
      console.error(err);
      alert("Failed to save decision");
    }
  };

  return (
    <div className="container">
      <h2>{scenario.title}</h2>
      <p>{scenario.description}</p>

      {scenario.results.map((opt, index) => (
        <div key={index} className="result-card">
          <h3>{opt.name}</h3>

          <h4>Short-Term Pros</h4>
          <ul>
            {opt.shortPros.map((p, i) => <li key={i}>{p}</li>)}
          </ul>

          <h4>Short-Term Cons</h4>
          <ul>
            {opt.shortCons.map((c, i) => <li key={i}>{c}</li>)}
          </ul>

          <h4>Long-Term Pros</h4>
          <ul>
            {opt.longPros.map((p, i) => <li key={i}>{p}</li>)}
          </ul>

          <h4>Long-Term Cons</h4>
          <ul>
            {opt.longCons.map((c, i) => <li key={i}>{c}</li>)}
          </ul>

          <button
            className="button"
            onClick={() => handleDecision(opt.name)}
          >
            Choose this option
          </button>
        </div>
      ))}

      <h3>Or enter your own decision:</h3>

      <input
        className="input"
        value={customDecision}
        onChange={(e) => setCustomDecision(e.target.value)}
        placeholder="Custom decision"
      />

      <button
        className="button"
        onClick={() => handleDecision(customDecision)}
      >
        Save Custom Decision
      </button>
    </div>
  );
}

export default Results;