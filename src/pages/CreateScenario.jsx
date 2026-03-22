import { useState } from "react";
import { useNavigate } from "react-router-dom";

function CreateScenario() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [options, setOptions] = useState(["", ""]);

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
    if (!title || !description || options.some(opt => !opt)) {
      alert("Please fill all required fields");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title,
          description,
          options
        })
      });

      if (!response.ok) throw new Error("Failed to analyze scenario");

      const results = await response.json();

      const newScenario = {
        id: Date.now(),
        title,
        description,
        options,
        results,
        finalDecision: null,
        reflection: ""
      };

      const existing = JSON.parse(localStorage.getItem("scenarios")) || [];
      localStorage.setItem(
        "scenarios",
        JSON.stringify([...existing, newScenario])
      );

      navigate("/results", { state: newScenario });

    } catch (err) {
      console.error(err);
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

      <button className="button" onClick={handleSubmit}>
        Generate Pros & Cons
      </button>
    </div>
  );
}

export default CreateScenario;