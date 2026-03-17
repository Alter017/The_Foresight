function Account() {
  const mockUser = {
    id: 1,
    name: "Mitali Bangre",
    email: "mitali.bangre@example.com",
    dob: "10th August 2025",
  };

  return (
    <div>
      <h2>Account Info</h2>

      <p><strong>User ID:</strong> {mockUser.id}</p>
      <p><strong>Name:</strong> {mockUser.name}</p>
      <p><strong>Email:</strong> {mockUser.email}</p>
      <p><strong>Date of Birth:</strong> {mockUser.dob}</p>

      <button onClick={() => alert("Delete account (coming soon)")}>
        Delete Account
      </button>
    </div>
  );
}

export default Account;