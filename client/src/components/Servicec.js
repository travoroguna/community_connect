import React, { useRef, useState } from "react";
import "../css/Service.css";
import ServiceItem from "./ServiceItem";

const Service = () => {
  const arr = [1, 2, 3, 4, 5, 6];
  const [translateX, setTranslateX] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);

  const slidesRef = useRef(null);
  const [scrollX, setScrollX] = useState(0);

  const handleScroll = () => {
    const slides = slidesRef.current;
    setScrollX(slides.scrollLeft);
  };

  const handlePrevClick = () => {
    const slides = slidesRef.current;
    slides.scrollBy(-slides.offsetwidth, 0);
  };

  function handleMouseDown(e) {
    setIsDragging(true);
    setStartX(e.clientX);
  }

  function handleMouseMove(e) {
    if (isDragging) {
      const deltaX = e.clientX - startX;
      setTranslateX((prev) => prev + deltaX);
      setStartX(e.clientX);
    }
  }

  function handleMouseUp() {
    setIsDragging(false);
  }

  function handleTouchStart(e) {
    setIsDragging(true);
    setStartX(e.touches[0].clientX);
  }

  function handleTouchMove(e) {
    if (isDragging) {
      const deltaX = e.touches[0].clientX - startX;
      setTranslateX((prev) => prev + deltaX);
      setStartX(e.touches[0].clientX);
    }
  }

  function handleTouchEnd() {
    setIsDragging(false);
  }

  return (
    <div
      className="service"
      // onMouseDown={handleMouseDown}
      // onMouseMove={handleMouseMove}
      // onMouseUp={handleMouseUp}
      // onTouchStart={handleTouchStart}
      // onTouchMove={handleTouchMove}
      // onTouchEnd={handleTouchEnd}
    >
      <div
        className="sliding-element"
        ref={slidesRef}
        onScroll={handleScroll}
        // style={{ transform: `translateX(${translateX}px)` }}
      >
        {arr.map((product, index) => (
          <ServiceItem />
        ))}
      </div>
      <button className="prev" onClick={handlePrevClick}>
        &lt;
      </button>
    </div>
  );
};

export default Service;
