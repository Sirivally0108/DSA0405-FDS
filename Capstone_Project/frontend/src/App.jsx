import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import Upload from "./pages/Upload.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Analysis from "./pages/Analysis.jsx";
import Charts from "./pages/Charts.jsx";
import Reports from "./pages/Reports.jsx";
import Prediction from "./pages/Prediction.jsx";

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/charts" element={<Charts />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/prediction" element={<Prediction />} />
        <Route
          path="*"
          element={
            <div className="page">
              <div className="page-content" style={{ paddingTop: 80 }}>
                <h2 style={{ color: "white" }}>Page not found</h2>
                <p style={{ color: "rgba(255,255,255,0.7)", marginTop: 8 }}>
                  That route doesn't exist in AgriVision.
                </p>
              </div>
            </div>
          }
        />
      </Routes>
    </>
  );
}
