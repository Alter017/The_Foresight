import "./Results.css";

import { useEffect, useState } from "react";

function History() {
  const [scenarios, setScenarios] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) {
          alert("User not logged in");
          return;
        }

        const response = await fetch(`http://127.0.0.1:5000/history/${user.id}`);
        if (!response.ok) throw new Error("Failed to fetch history");

        const data = await response.json();
        setScenarios(data);

      } catch (err) {
        console.error(err);
        alert("Could not load history");
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="container">
      <h2>History</h2>

      {scenarios.length === 0 ? (
        <p>No scenarios found</p>
      ) : (
        scenarios.map((s, i) => (
          <div key={i} className="result-card">
            <h3>{s.title}</h3>
            <p>
              <strong>Final Decision:</strong>{" "}
              {s.finalDecision || "None"}
            </p>
          </div>
        ))
      )}
    </div>
  );
}

export default History;