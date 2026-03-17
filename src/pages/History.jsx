import { useEffect, useState } from "react";

function History() {
  const [scenarios, setScenarios] = useState([]);

    useEffect(() => {
    const fetchHistory = async () => {
        try {
        const user = JSON.parse(localStorage.getItem("user"));
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
        <div>
        <h2>History</h2>

        {scenarios.map((s, i) => (
            <div key={i}>
            <h3>{s.title}</h3>
            <p>Final Decision: {s.finalDecision || "None"}</p>
            </div>
        ))}
        </div>
    );
}

export default History;