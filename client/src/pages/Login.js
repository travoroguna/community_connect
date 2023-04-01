import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "../css/Login.css";
import NavBar from "../components/NavBar";
import { signin } from "../api/ApiRoute";

const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [hasError, setHasError] = useState(false);

  const { username, password } = formData;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setHasError(false);
  };

  const submit = (e) => {
    e.preventDefault();

    axios
      .post(signin, formData)
      .then((res) => {
        console.log(res);
        setHasError(false);
      })
      .catch((err) => {
        console.log(err);
        setHasError(true);
      });
  };

  return (
    <div className="login" onSubmit={submit}>
      <NavBar />

      <main>
        <form>
          <img src="/images/sterling-cares.jpg" />

          <div className="form">
            <h2>Welcome Back!</h2>
            {hasError && <div className="error">Server error</div>}
            <input
              type="text"
              placeholder="Username"
              name="username"
              required
              value={username}
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
            <button type="submit">SIGN IN</button>
            <p>
              Don't have an account? <Link to="/signup">Sign Up</Link>
            </p>
          </div>
        </form>
      </main>
    </div>
  );
};

export default Login;
