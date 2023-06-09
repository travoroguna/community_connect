import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Event from "./pages/Event";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" exact element={<Home />} />
          <Route path="/signin" exact element={<Login />} />
          <Route path="/signup" exact element={<Register />} />
          <Route path="/event" exact element={<Event />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
