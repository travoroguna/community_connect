import React, { useState } from "react";
import { useNavigate } from "react-router";
import { eventapi } from "../api/ApiRoute";
import NavBar from "../components/NavBar";
import axios from "axios";
import "../css/Event.css";

const Event = () => {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    image: "",
    date: "",
    startTime: "",
    endTime: "",
    location: "",
    targetNumber: "",
    companyName: "",
    phoneNumber: "",
  });
  const [hasError, setHasError] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const {
    name,
    description,
    image,
    date,
    startTime,
    endTime,
    location,
    targetNumber,
    companyName,
    phoneNumber,
  } = formData;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const submit = (e) => {
    e.preventDefault();

    axios
      .post(eventapi, formData)
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
    <div className="event">
      <NavBar />
      <main>
        <form onSubmit={submit}>
          <h1>Event Creation form</h1>
          {hasError && (
            <div className="error">{error ? error : "Server error"}</div>
          )}
          <div className="container">
            <div className="left-section">
              <div className="label">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  name="name"
                  required
                  value={name}
                  onChange={handleChange}
                />
              </div>
              <div className="label">
                <label htmlFor="description">Description</label>
                <textarea
                  name="description"
                  id=""
                  value={description}
                  onChange={handleChange}
                ></textarea>
              </div>
              <div className="label">
                <label htmlFor="image">Upload Image</label>
                <input
                  type="file"
                  name="image"
                  required
                  value={image}
                  onChange={handleChange}
                />
              </div>
              <div className="label">
                <label htmlFor="date">Date</label>
                <input
                  type="date"
                  name="date"
                  value={date}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="label-time">
                <div className="label">
                  <label htmlFor="startTime">Start time</label>
                  <input
                    type="time"
                    name="startTime"
                    value={startTime}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="label">
                  <label htmlFor="endTime">End time</label>
                  <input
                    type="time"
                    name="endTime"
                    value={endTime}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
            </div>

            <div className="right-section">
              <div className="label">
                <label htmlFor="location">Location</label>
                <input
                  type="text"
                  name="location"
                  required
                  value={location}
                  onChange={handleChange}
                />
              </div>
              <div className="label">
                <label htmlFor="targetNumber">
                  Target number of Volunteers
                </label>
                <input
                  type="number"
                  name="targetNumber"
                  required
                  value={targetNumber}
                  onChange={handleChange}
                />
              </div>

              <div className="contact-details">
                <p>Contact Details</p>
                <div className="label">
                  <label htmlFor="companyName">
                    Company Name / Name of Organiser
                  </label>
                  <input
                    type="text"
                    name="companyName"
                    required
                    value={companyName}
                    onChange={handleChange}
                  />
                </div>
                <div className="label">
                  <label htmlFor="phoneNumber">Phone Number</label>
                  <input
                    type="number"
                    name="phoneNumber"
                    required
                    value={phoneNumber}
                    onChange={handleChange}
                  />
                </div>
              </div>
            </div>
          </div>
          <button type="submit">SUBMIT</button>
        </form>
      </main>
    </div>
  );
};

export default Event;
