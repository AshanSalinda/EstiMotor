import { Routes, Route } from 'react-router-dom';
import ModelTraining from '../pages/ModelTraining';
import AdminManagement from '../pages/AdminManagement.jsx';
import NotFoundPage from "../pages/NotFoundPage.jsx";
import ProtectedRoute from "./ProtectedRoute.jsx";

export default function AdminRoutes() {
    return (
        <Routes>
            <Route element={<ProtectedRoute />} >
                <Route path="/model-training" element={<ModelTraining />} />
                <Route path="/admin-management" element={<AdminManagement />} />
            </Route>
            <Route path="/*" element={<NotFoundPage />} />
        </Routes>
    )
}
