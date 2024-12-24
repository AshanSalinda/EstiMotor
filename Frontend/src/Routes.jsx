import React from 'react';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ModelTraining from './pages/ModelTraining.jsx';
import Login from './pages/Login.jsx';
import Home from './pages/Home.jsx';

export default function Router() {
    const router = createBrowserRouter([
        {
            path: "/",
            element: <Home/>,
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
