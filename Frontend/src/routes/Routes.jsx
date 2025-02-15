import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from '../pages/Home.jsx';

const AdminRoutes = lazy(() => import("./AdminRoutes.jsx"));
const Login = lazy(() => import("../pages/Login.jsx"));

export default function Router() {
    return (
        <BrowserRouter>
            <Suspense fallback={<div className="text-red-500">Loading...</div>}>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/*" element={<AdminRoutes />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    )
}
