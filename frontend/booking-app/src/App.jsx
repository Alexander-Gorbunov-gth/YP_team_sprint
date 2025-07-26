import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar/Sidebar";
import Header from "./components/Header/Header";

import EventsPage from './pages/events/EventsPage'; // <-- импорт OK

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ display: "flex", height: "100vh" }}>
        <Sidebar />

        <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
          <Header />

          <main style={{ flex: 1, padding: "30px", backgroundColor: "#f9fafb", overflow: "auto", display: "flex", flexDirection: "column" }}>
            <Routes>
              <Route path="/" element={<h1>Добро пожаловать 👋</h1>} />
              <Route path="/events" element={<EventsPage />} />
              <Route path="/my-events" element={<EventsPage />} />
              <Route path="/bookings" element={<h1>Бронирования</h1>} />
              <Route path="/subscriptions" element={<h1>Подписки</h1>} />
              <Route path="/notifications" element={<h1>Уведомления</h1>} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}