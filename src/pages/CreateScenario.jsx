import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generateProsCons } from "../services/api";

function CreateScenario() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [options, setOptions] = useState(["", ""]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleOptionChange = (index, value) => {
    const newOptions = [...options];
    newOptions[index] = value;
    setOptions(newOptions);
  };

  const addOption = () => {
    setOptions([...options, ""]);
  };

  const handleSubmit = async () => {
    console.log("Submit clicked");

    if (!title || !description || options.some(opt => !opt.trim())) {
      alert("Please fill all required fields");
      return;
    }

    const cleanOptions = options.filter(opt => opt.trim() !== "");
    setLoading(true);
    
    const storedUser = JSON.parse(localStorage.getItem("user") || "null");

    try {
      const results = await generateProsCons({
        title,
        description,
        options: cleanOptions,
        user_id: storedUser?.id || null
      });

      if (!Array.isArray(results)) {
        alert("AI failed. Try again.");
        setLoading(false);
        return;
      }

      let realId = null;

      if (storedUser) {
        const saveRes = await fetch("http://localhost:5000/scenario/save", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: storedUser.id,
            title,
            scenario_text: description,
            options: cleanOptions,
            pros_cons: results
          })
        });

        const saveData = await saveRes.json();

        console.log("SAVE RESPONSE:", saveData);

        if (!saveRes.ok) {
          throw new Error("Failed to save scenario");
        }

        realId = saveData.scenario_id;
      }

      const newScenario = {
        id: realId, 
        title,
        description,
        options: cleanOptions,
        results,
        finalDecision: null,
        reflection: ""
      };

      setLoading(false);
      navigate("/results", { state: newScenario });

    } catch (err) {
      console.error(err);
      setLoading(false);
      alert("Error analyzing scenario. Try again.");
    }
  };

  return (
    <div className="container">
      <h1>Create Scenario</h1>

      <input
        className="input"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <textarea
        className="input"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <h3>Options</h3>

      {options.map((opt, i) => (
        <input
          key={i}
          className="input"
          value={opt}
          onChange={(e) => handleOptionChange(i, e.target.value)}
          placeholder={`Option ${i + 1}`}
        />
      ))}

      <button className="button" onClick={addOption}>
        + Add Option
      </button>

      <button
        className="button"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      
    </div>
  );
}

export default CreateScenario;
