export const generateProsCons = async (scenario) => {
  const res = await fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(scenario),
  });

  return res.json();
};