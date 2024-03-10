import { React, useEffect, useLocation, useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  BrowserRouter,
} from "react-router-dom";

import Home from "./pages/Home";
import Recommend from "./pages/Recommend";

import Navbar from "./components/Navbar";
import Callback from "./Callback";
import Authorize from "./components/Authorize";

function AppRouter() {
  const [authorized, setAuthorized] = useState(false);
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route
          path="/recommend"
          element={<Recommend authorized={authorized} />}
        />
        <Route
          path="/callback"
          element={<Callback setAuthorized={setAuthorized} />}
        />
        <Route path="/authorize" element={<Authorize />} />
      </Routes>
    </Router>
  );
}

export default AppRouter;
