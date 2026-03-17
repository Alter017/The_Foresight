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

  const handleSubmit = () => {
    if (!title || !description || options.length < 2) {
      alert("Please fill all required fields");
      return;
    }

  const handleSubmit = async () => {
    if (!title || !description || options.length < 2) {
      alert("Please fill all required fields");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description, options }),
      });

      if (!response.ok) throw new Error("Failed to analyze scenario");

      const results = await response.json(); // should match the structure: [{name, shortPros, shortCons, longPros, longCons}, ...]
      
      const newScenario = {
        id: Date.now(),
        title,
        description,
        options,
        results,
        finalDecision: null,
        reflection: ""
      };

      // Save in localStorage for frontend history UI
      const existing = JSON.parse(localStorage.getItem("scenarios")) || [];
      localStorage.setItem("scenarios", JSON.stringify([...existing, newScenario]));

      navigate("/results", { state: newScenario });

    } catch (err) {
      console.error(err);
      alert("Error analyzing scenario. Try again.");
    }
  };

    const newScenario = {
      id: Date.now(), // unique ID
      title,
      description,
      options,
      results: mockResults,
      finalDecision: null,
      reflection: ""
    };

    const existing = JSON.parse(localStorage.getItem("scenarios")) || [];

    localStorage.setItem(
      "scenarios",
      JSON.stringify([...existing, newScenario])
    );

    navigate("/results", {
      state: newScenario
    });
  };

  return (
    <div>
      <h2>Create Scenario</h2>

      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <h3>Options</h3>
      {options.map((opt, i) => (
        <input
          key={i}
          value={opt}
          onChange={(e) => handleOptionChange(i, e.target.value)}
          placeholder={`Option ${i + 1}`}
        />
      ))}

      <button onClick={addOption}>+ Add Option</button>
      <br />
      <button onClick={handleSubmit}>Generate Pros & Cons</button>
    </div>
  );
}

export default CreateScenario;