import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";

import Login from "./pages/auth/Login";
import StudentDashboard from "./pages/student/StudentDashboard";
import HODDashboard from "./pages/hod/HODDashboard";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<ProtectedRoute allowedRoles={["STUDENT"]} />}>
        <Route path="/student/dashboard" element={<StudentDashboard />} />
      </Route>

      <Route element={<ProtectedRoute allowedRoles={["HOD"]} />}>
        <Route path="/hod/dashboard" element={<HODDashboard />} />
      </Route>

      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
