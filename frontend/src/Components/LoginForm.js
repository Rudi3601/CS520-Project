// LoginForm.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    // Check if username and password match your criteria
    if (username === 'yourUsername' && password === 'yourPassword') {
      // Navigate to another page if credentials are valid
      navigate('/');
    } else {
      // Handle incorrect credentials (display an error, etc.)
      console.log('Invalid credentials');
    }
  };

  return (
    <div>
      <h1>Login</h1>1
      <label>
        Username:
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </label>
      <br />
      <label>
        Password:
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </label>
      <br />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginForm;