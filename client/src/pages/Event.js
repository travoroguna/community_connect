import React from "react";
import NavBar from "../components/NavBar";
// import "../css/Event.css"

const Event = () => {
  return (
    <div className="event">
      <NavBar />
      <main>
        <h1>Event Creation form</h1>
        <form>
          <div className="left-section">
            <div className="label">
              <label htmlFor="name">Name</label>
              <input type="text" name="name" required />
            </div>
            <div className="label">
              <label htmlFor="description">Description</label>
              <textarea name="description" id=""></textarea>
            </div>
            <div className="label">
              <label htmlFor="image">Upload Image</label>
              <input type="file" name="image" required />
            </div>
            <div className="label">
              <label htmlFor="date">Date</label>
              <input type="date" name="date" />
            </div>
            <div className="label-time">
              <div className="label">
                <label htmlFor="startTime">Start time</label>
                <input type="time" name="startTime" />
              </div>
              <div className="label">
                <label htmlFor="endTime">End time</label>
                <input type="time" name="endTime" />
              </div>
            </div>
          </div>
        </form>
      </main>
    </div>
  );
};

export default Event;
