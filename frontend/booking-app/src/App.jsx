import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar/Sidebar";
import Header from "./components/Header/Header";

import EventsPage from './pages/events/EventsPage'; // <-- импорт OK
import SubscriptionsPage from "./pages/subscriptions/SubscriptionsPage";
import NewBookingPage from "./pages/booking/NewBookingPage";
import BookingsPage from "./pages/booking/BookingsPage";
import BookingDetailPage from "./pages/booking/BookingDetailPage";
import MyEventsPage from "./pages/my_events/MyEventsPage";
import CreateEventPage from "./pages/my_events/CreateEventPage";
import AddAddressPage from "./pages/address/AddAddressPage";
import EditEventPage from "./pages/my_events/EditEventPage";

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
              <Route path="/events/new" element={<CreateEventPage />} />
              <Route path="/addresses/new" element={<AddAddressPage />} />
              <Route path="/my-events" element={<MyEventsPage />} />
              <Route path="/bookings" element={<BookingsPage />} />
              <Route path="/bookings/:id" element={<BookingDetailPage />} />
              <Route path="/bookings/new" element={<NewBookingPage />} />
              <Route path="/subscriptions" element={<SubscriptionsPage />} />
              <Route path="/events/:id" element={<EditEventPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
