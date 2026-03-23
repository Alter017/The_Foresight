import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

function History() {
  const navigate = useNavigate();
  const [scenarios, setScenarios] = useState([]);
  const [isCheckingLogin, setIsCheckingLogin] = useState(true);

  useEffect(() => {
    if (!localStorage.getItem("loggedIn")) {
      navigate("/login");
    } else {
      setIsCheckingLogin(false);
    }
  }, [navigate]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) {
          alert("User not logged in");
          return;
        }

        const response = await fetch(
          `http://localhost:5000/scenario/history?user_id=${user.id}`
        );

        if (!response.ok) throw new Error("Failed to fetch history");

        const data = await response.json();
        setScenarios(data.scenarios);

      } catch (err) {
        console.error(err);
        alert("Could not load history");
      }
    };

    if (!isCheckingLogin) {
      fetchHistory();
    }
  }, [isCheckingLogin]);

  if (isCheckingLogin) {
    return null; // or a loading spinner
  }

  return (
    <div className="container" style={{ maxHeight: "80vh", overflowY: "auto" }}>
      <h2>History</h2>

      {scenarios.length === 0 ? (
        <p>No scenarios found</p>
      ) : (
        scenarios.map((s) => (
          <div key={s.id} className="result-card">
            <h3>{s.title}</h3>

            <p><strong>Date:</strong> {new Date(s.created_at).toLocaleString()}</p>

            <p><strong>Description:</strong> {s.scenario_text}</p>

            <p><strong>Options:</strong></p>
            <ul>
              {(s.options || []).map((opt, i) => (
                <li key={i}>{opt}</li>
              ))}
            </ul>

            <p>
              <strong>Chosen Decision:</strong>{" "}
              {s.final_decision_text || "None"}
            </p>

            {(s.pros_cons || []).map((opt, index) => (
              <div key={index} style={{ marginTop: "10px" }}>
                <h4>{opt.name || "Option"}</h4>

                <strong>Short Pros:</strong>
                <ul>
                  {(opt.shortPros || []).map((p, i) => <li key={i}>{p}</li>)}
                </ul>

                <strong>Short Cons:</strong>
                <ul>
                  {(opt.shortCons || []).map((c, i) => <li key={i}>{c}</li>)}
                </ul>

                <strong>Long Pros:</strong>
                <ul>
                  {(opt.longPros || []).map((p, i) => <li key={i}>{p}</li>)}
                </ul>

                <strong>Long Cons:</strong>
                <ul>
                  {(opt.longCons || []).map((c, i) => <li key={i}>{c}</li>)}
                </ul>
              </div>
            ))}

            <textarea
              placeholder="Add reflection..."
              defaultValue={s.reflection_note || ""}
              onBlur={async (e) => {
                const note = e.target.value;

                try {
                  await fetch(
                    `http://localhost:5000/scenario/${s.id}/reflection-note`,
                    {
                      method: "PUT",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({
                        user_id: JSON.parse(localStorage.getItem("user")).id,
                        reflection_note: note,
                      }),
                    }
                  );
                } catch (err) {
                  console.error(err);
                }
              }}
              className="input"
            />
          </div>
        ))
      )}
    </div>
  );
}

export default History;
