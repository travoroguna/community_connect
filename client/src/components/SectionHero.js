import React from "react";
import { Link } from "react-router-dom";
import "../css/SectionHero.css";

const SectionHero = () => {
  return (
    <div className="hero">
      <div className="signup-container">
        <h1>Make an impact in what YOU believe in!</h1>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Minima,
          aspernatur exercitationem. Quo rerum obcaecati minus quidem eum
          voluptatum dicta fuga?
        </p>
        <Link to="/signup" className="btn">
          Sign up
        </Link>
      </div>
    </div>
  );
};

export default SectionHero;
