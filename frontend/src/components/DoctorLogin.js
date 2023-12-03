// LoginPage.js
import React, { useState } from 'react';
import './DoctorLogin.css'

const DoctorLogin = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // Add your authentication logic here (e.g., send credentials to a server)
    console.log('Username:', username);
    console.log('Password:', password);
    // You can redirect the user or perform other actions based on successful login
  };

  return (
    <div>
      <h2 className="center-container">Doctor Login Page</h2>
      <form className="input-box">
        <label>
          Username:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <br />
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <br />
        <button type="button" onClick={handleLogin}>
          Login
        </button>
      </form>
    </div>
  );
};

export default DoctorLogin;