import React from "react";
import NavBar from "../components/NavBar";
import SectionHero from "../components/SectionHero";
import Service from "../components/Service";
import "../css/Home.css";

const Home = () => {
  return (
    <div className="home">
      <NavBar />
      <SectionHero />
      <Service />
    </div>
  );
};

export default Home;
