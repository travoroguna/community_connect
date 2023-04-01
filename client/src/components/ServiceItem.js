import React from "react";
import { Link } from "react-router-dom";

const ServiceItem = () => {
  return (
    <div className="service-item">
      <div className="img"></div>
      <div className="service-content">
        <h2>Help clean our rivers</h2>
        <p>
          By leading a waterway cleanup effort with others in your community,
          you can help make your river or stream a safer, healthier place for
          wildlife and people.
        </p>
        <Link className="btn" to={"/"}>
          JOIN
        </Link>
      </div>
    </div>
  );
};

export default ServiceItem;
