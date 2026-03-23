import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) throw new Error("Login failed");

      const data = await response.json();

      localStorage.setItem("user", JSON.stringify(data.user));
      localStorage.setItem("loggedIn", "true");

      alert("Login successful!");
      navigate("/dashboard");

    } catch (err) {
      console.error(err);
      alert("Login failed");
    }
  };

  return (
    <div className="container">
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <input
          className="input"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          className="input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button className="button" type="submit">
          Login
        </button>
        <p>
          Don’t have an account?{" "}
          <a href="/signup" className="link">
            Sign up
          </a>
        </p>
      </form>
    </div>
  );
}

export default Login;
