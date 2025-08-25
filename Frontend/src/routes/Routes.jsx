import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from '../pages/Home.jsx';
import LoadingPage from "../pages/LoadingPage.jsx";

const AdminRoutes = lazy(() => import("./AdminRoutes.jsx"));
const Login = lazy(() => import("../pages/Login.jsx"));

export default function Router() {
    return (
        <BrowserRouter future={{
            v7_startTransition: true,
            v7_relativeSplatPath: true
        }}>
            <Suspense fallback={<LoadingPage />} >
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/*" element={<AdminRoutes />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    )
}
