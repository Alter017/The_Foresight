import { useLocation } from "react-router-dom";

function ScenarioDetail() {
  const { state } = useLocation();

  if (!state) {
    return <h2>No scenario data found</h2>;
  }

  const scenario = state;

  return (
    <div>
      <h2>{scenario.title}</h2>
      <p>{scenario.description}</p>

      {scenario.results.map((opt, i) => (
        <div key={i}>
          <h3>{opt.name}</h3>

          <h4>Short-Term Pros</h4>
          <ul>{opt.shortPros.map((p, idx) => <li key={idx}>{p}</li>)}</ul>

          <h4>Short-Term Cons</h4>
          <ul>{opt.shortCons.map((c, idx) => <li key={idx}>{c}</li>)}</ul>

          <h4>Long-Term Pros</h4>
          <ul>{opt.longPros.map((p, idx) => <li key={idx}>{p}</li>)}</ul>

          <h4>Long-Term Cons</h4>
          <ul>{opt.longCons.map((c, idx) => <li key={idx}>{c}</li>)}</ul>
        </div>
      ))}

      <h3>Final Decision:</h3>
      <p>{scenario.finalDecision || "Not selected"}</p>

      <h3>Reflection Notes:</h3>
      <p>{scenario.reflection || "No notes yet"}</p>
    </div>
  );
}

export default ScenarioDetail;