// LoginPage.js
import React, { useState } from 'react';
import './DoctorLogin.css'
import httpClient from "../httpClient";
import { useNavigate } from "react-router-dom";

const DoctorLogin = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [authenticated, setauthenticated] = useState(localStorage.getItem(localStorage.getItem("authenticated")|| false));
  // TODO: Mock Data, Delete ASAP!
  const users = [{ username: "Jane", password: "testpassword" }];

  const handleLogin = (e) => {
    e.preventDefault()
    const account = users.find((user) => user.username === username);
    if (account && account.password === password) {
        setauthenticated(true)
        localStorage.setItem("authenticated", true);
        navigate("/DoctorPortal");
    }
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
}

export default DoctorLogin;