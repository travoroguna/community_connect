import React from "react";
import { Link } from "react-router-dom";
import "../css/SectionHero.css";

const SectionHero = () => {
  return (
    <div className="hero">
      <div className="signup-container">
        <h1>Make an impact in what YOU believe in!</h1>
        <p>
          Our social impact project aims to empower individuals and communities to make a difference in the causes they believe in. With our app, you can easily donate to organizations making a positive impact, organize your own charity events, or advertise upcoming events in your area. By coming together and taking action, we can create a better world for ourselves and future generations. Join us in making a difference today!
        </p>
        <Link to="/signup" className="btn">
          Sign up
        </Link>
      </div>
    </div>
  );
};

export default SectionHero;
