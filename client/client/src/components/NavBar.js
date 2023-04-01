import React from "react";
import { Link } from "react-router-dom";
import "../css/NavBar.css";

const NavBar = () => {
  return (
    <div className="nav">
      <div className="logo">Logo Name</div>
      <ul>
        <li>
          <Link to="/">Events</Link>
        </li>
        <li>
          <Link to="/">Donor Basics</Link>
        </li>
        <li>
          <Link to="/">About Us</Link>
        </li>
        <li>
          <Link to="/signin">Sign In</Link>
        </li>
      </ul>
    </div>
  );
};

export default NavBar;
