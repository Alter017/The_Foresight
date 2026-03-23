export const generateProsCons = async (data) => {
  const response = await fetch("http://localhost:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error("Failed to analyze scenario");
  }

  const results = await response.json();
  return results;
};