import React from 'react';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import AdminLayout from './sections/AdminLayout.jsx';
import ModelTraining from './pages/ModelTraining.jsx';
import Login from './pages/Login.jsx';

export default function Router() {
    const router = createBrowserRouter([
        {
            path: "/",
            element: <AdminLayout/>,
        },
        {
            path: "/model-training",
            element: <ModelTraining/>,
        },
        {
            path: "/login",
            element: <Login/>,
        }
    ]);

    return (
        <RouterProvider router={router} />
    )
}
