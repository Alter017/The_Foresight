import "./Account.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Profile() {
  const [user, setUser] = useState(null);

  const [newUsername, setNewUsername] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");

    if (!storedUser) {
      navigate("/login");
      return;
    }

    setUser(JSON.parse(storedUser));
  }, [navigate]);

  const handleUsernameUpdate = async () => {
    if (!newUsername.trim()) {
      alert("Username cannot be empty");
      return;
    }

    if (newUsername.length < 3) {
      alert("Username must be at least 3 characters");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/auth/account/username", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userId: user.id,
        username: newUsername
      })
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.ok) {
      const updatedUser = { ...user, username: newUsername };
      setUser(updatedUser);
      localStorage.setItem("user", JSON.stringify(updatedUser));
      setNewUsername("");
    }
  };

  const handlePasswordUpdate = async () => {
    if (!currentPassword || !newPassword || !confirmNewPassword) {
      alert("All fields required");
      return;
    }

    if (newPassword.length < 3) {
      alert("Password must be at least 3 characters");
      return;
    }

    if (newPassword !== confirmNewPassword) {
      alert("Passwords do not match");
      return;
    }

    const res = await fetch("http://127.0.0.1:5000/auth/account/password", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userId: user.id,
        currentPassword,
        newPassword,
        confirmNewPassword
      })
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.ok) {
      setCurrentPassword("");
      setNewPassword("");
      setConfirmNewPassword("");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("loggedIn");
    navigate("/login");
  };

  if (!user) return <p>Loading...</p>;

  return (
    <div className="profile-container">
      
      <div className="profile-left">
        <h1>Account</h1>
        <p><strong>User ID:</strong> {user.id}</p>
        <p><strong>Username:</strong> {user.username}</p>
        <p><strong>Email:</strong> {user.email}</p>

        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="profile-right">

        <h3>Update Username</h3>
        <input
          placeholder="New username"
          value={newUsername}
          onChange={(e) => setNewUsername(e.target.value)}
        />
        <button onClick={handleUsernameUpdate}>
          Update Username
        </button>

        <h3>Update Password</h3>

        <input
          type="password"
          placeholder="Current password"
          value={currentPassword}
          onChange={(e) => setCurrentPassword(e.target.value)}
        />

        <input
          type="password"
          placeholder="New password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
        />

        <input
          type="password"
          placeholder="Confirm new password"
          value={confirmNewPassword}
          onChange={(e) => setConfirmNewPassword(e.target.value)}
        />

        <button onClick={handlePasswordUpdate}>
          Update Password
        </button>

      </div>
    </div>
  );
}

export default Profile;
