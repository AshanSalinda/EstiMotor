import { Navigate, Outlet } from "react-router-dom";
import useAdminInfo from "../hooks/useAdminInfo.js";


export default function ProtectedRoute() {
    const adminInfo = useAdminInfo();

    if (!adminInfo) {
        return <Navigate to="/login" replace />;
    }

    return <Outlet />; // renders child routes
}
