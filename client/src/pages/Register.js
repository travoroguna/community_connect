import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "../css/Login.css";
import NavBar from "../components/NavBar";

const Register = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    username: "",
  });

  const { email, password, username } = formData;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const submit = (e) => {
    e.preventDefault();
  };

  return (
    <div className="login" onSubmit={submit}>
      <NavBar />

      <main>
        <form>
          <img src="/images/sterling-cares.jpg" />

          <div className="form">
            <h2>Create Account</h2>
            <input
              type="text"
              placeholder="Username"
              name="username"
              required
              value={username}
              onChange={handleChange}
            />
            <input
              type="email"
              placeholder="Email"
              name="email"
              required
              value={email}
              onChange={handleChange}
            />
            <input
              type="password"
              placeholder="Password"
              name="password"
              required
              value={password}
              onChange={handleChange}
            />
            <button type="submit">SIGN UP</button>
            <p>
              Already Have An Account? <Link to="/signin">Sign In</Link>
            </p>
          </div>
        </form>
      </main>
    </div>
  );
};

export default Register;
