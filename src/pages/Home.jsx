import "./Home.css";
import sideImage from "../assets/robot.png";


function Home() {
  return (
    <div className="container home-container">
      
      <div className="home-image">
        <img src={sideImage} alt="visual" />
      </div>

      <div className="home-content">
        <h1>Foresight</h1>
        <p>Feeling overwhelmed by a decision? Let’s help you see the pros and cons clearly</p>

        <a href="/create" className="button">Create Scenario</a>
        <a href="/login" className="button">Login</a>
        <a href="/signup" className="button">Sign Up</a>
      </div>

    </div>
  );
}


export default Home;