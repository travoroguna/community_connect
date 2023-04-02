import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "../css/Login.css";
import NavBar from "../components/NavBar";
import { signin } from "../api/ApiRoute";

const Login = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [hasError, setHasError] = useState(false);
  const [error, setError] = useState("");

  const { username, password } = formData;

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
    setHasError(false);
  };

  const submit = (e) => {
    e.preventDefault();

    if (username.length > 8) {
      setError("Username must be at least 8 characters long.");
      setHasError(true);
    } else
      axios
        .post(signin, formData)
        .then((res) => {
          console.log(res);
          navigate("/");
          setHasError(false);
        })
        .catch((err) => {
          console.log(err);
          setHasError(true);
          if (err.data.message) {
            setError(err.data.message);
            return err;
          }

          if (err.message === "Network Error") {
            setError("Check your internet connection");
            return err;
          } else {
            setError("Server error");
            return err;
          }
        });
  };

  return (
    <div className="login" onSubmit={submit}>
      <NavBar />

      <main>
        <form>
          <img src="/images/sterling-cares.jpg" alt="" />

          <div className="form">
            <h2>Welcome Back!</h2>
            {hasError && (
              <div className="error">{error ? error : "Server error"}</div>
            )}
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
