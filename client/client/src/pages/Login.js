import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios"
import "../css/Login.css";

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });

  const { email, password } = formData;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const sumbit = (e) => {
    e.preventDefault();

    
  };

  return (
    <div className="login">
      <form>
        <h2>SIGN IN TO YOUR ACCOUNT</h2>
        {/* <input type="text" placeholder="username" name="username" /> */}
        <input
          type="email"
          placeholder="email"
          name="email"
          required
          value={email}
          onChange={handleChange}
        />
        <input
          type="password"
          placeholder="password"
          name="password"
          required
          value={password}
          onChange={handleChange}
        />
        <button type="submit">SIGN IN</button>
        <p>
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </p>
      </form>
    </div>
  );
};

export default Login;
