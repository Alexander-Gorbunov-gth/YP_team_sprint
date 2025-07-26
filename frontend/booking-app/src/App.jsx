import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { Navigate, Outlet } from "react-router-dom";
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
import EditAddressPage from "./pages/address/EditAddressPage";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage"


function PrivateRoute() {
  const token = localStorage.getItem("access_token");
  return token ? <Outlet /> : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}

function AppLayout() {
  const location = useLocation();
  const hideLayout = location.pathname === "/login" || location.pathname === "/register";

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {!hideLayout && <Sidebar />}

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        {!hideLayout && <Header />}

        <main style={{ flex: 1, backgroundColor: "#f9fafb", overflow: "auto", display: "flex", flexDirection: "column" }}>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            <Route element={<PrivateRoute />}>
              <Route path="/" element={<h1>Добро пожаловать 👋</h1>} />
              <Route path="/events" element={<EventsPage />} />
              <Route path="/events/new" element={<CreateEventPage />} />
              <Route path="/addresses/new" element={<AddAddressPage />} />
              <Route path="/edit-address/:id" element={<EditAddressPage />} />
              <Route path="/my-events" element={<MyEventsPage />} />
              <Route path="/bookings" element={<BookingsPage />} />
              <Route path="/bookings/:id" element={<BookingDetailPage />} />
              <Route path="/bookings/new" element={<NewBookingPage />} />
              <Route path="/subscriptions" element={<SubscriptionsPage />} />
              <Route path="/events/:id" element={<EditEventPage />} />
            </Route>
          </Routes>
        </main>
      </div>
    </div>
  );
}
