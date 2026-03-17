import "./Home.css";

function Home() {
  return (
    <div className="container">
      <h1>Foresight</h1>
      <br></br>
      <p>Feeling overwhelmed by a decision? Let’s help you see the pros and cons clearly.</p>
      <a href="/create" className="button">Create Scenario</a>
      <a href="/login" className="button">Login</a>
      <a href="/signup" className="button">Sign Up</a>
    </div>
  );
}

export default Home;