import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "../css/Login.css";
import NavBar from "../components/NavBar";
import { signup } from "../api/ApiRoute";

const Register = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    username: "",
  });
  const [hasError, setHasError] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const { email, password, username } = formData;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError("");
    setHasError(false);
  };

  const submit = (e) => {
    e.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (username.length > 8) {
      setError("Username must be at least 8 characters long.");
      setHasError(true);
    } else if (password.length < 6) {
      setError("Password must be more than 5 characters");
      setHasError(true);
    } else if (!emailRegex.test(email) || email.endsWith("@gmail.com")) {
      setError("Please enter a valid email address");
    } else
      axios
        .post(signup, formData)
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
        <form onSubmit={submit}>
          <img src="/images/sterling-cares.jpg" alt="" />

          <div className="form">
            <h2>Create Account</h2>
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
