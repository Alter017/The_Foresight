import { useLocation } from "react-router-dom";
import { useState } from "react";

function Results() {
  const { state } = useLocation();

  const scenario =
    state ||
    JSON.parse(localStorage.getItem("scenarios"))?.slice(-1)[0];

  const [customDecision, setCustomDecision] = useState("");

  const handleDecision = async (choice) => {
    if (!choice) {
      alert("Please enter a decision");
      return;
    }

    const user = JSON.parse(localStorage.getItem("user"));

    if (!user) {
      alert("You must be logged in to save a decision");
      return;
    }

    try {
      const res = await fetch(
        `http://localhost:5000/scenario/${scenario.id}/final-decision`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: user.id,           
            final_decision_text: choice      
          }),
        }
      );
      

      if (!res.ok) {
        const err = await res.json();
        console.error("BACKEND ERROR:", err);
        console.log("SCENARIO ID:", scenario.id);
        throw new Error("Failed to save decision");
      }

      console.log("SCENARIO ID:", scenario.id);
      alert(`Decision saved: ${choice}`);

    } catch (err) {
      console.error(err);
      console.log("SCENARIO ID:", scenario.id);
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
