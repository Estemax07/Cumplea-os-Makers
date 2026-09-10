import { Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import AIChat from "./components/AIChat";
import CalendarPage from "./pages/CalendarPage";
import AdminPage from "./pages/AdminPage";

export default function App() {
  return (
    <div>
      <NavBar />
      <Routes>
        <Route path="/" element={<CalendarPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
      <AIChat />
    </div>
  );
}
