import "./Home.css";
import sideImage from "../assets/robot.png";

import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

function Dashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem("loggedIn")) {
      navigate("/login");
    }
  }, [navigate]);

  return (
    <div className="container home-container">
      
      <div className="home-image">
        <img src={sideImage} alt="visual" />
      </div>

      <div className="home-content">
        <h1>Foresight</h1>
        <p>Feeling overwhelmed by a decision? Let’s help you see the pros and cons clearly</p>

        <a href="/create" className="button">Analyze Scenario</a>
        <a href="/history" className="button">View History</a>
        <a href="/profile" className="button">Profile</a>
      </div>

    </div>
  );
}

export default Dashboard;
