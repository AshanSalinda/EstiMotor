import React from 'react';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import AdminLayout from './sections/AdminLayout.jsx';
import ManualTraining from './pages/ManualTraining.jsx';

export default function Router() {
    const router = createBrowserRouter([
        {
            path: "/",
            element: <AdminLayout/>,
            children: [
                { index: true, element: <ManualTraining/>, handle: { title: 'Manual Training' } },
                { path: "about", element: <h1>About</h1>, handle: { title: 'About - EstiMotor' } },
                { path: "contact", element: <h1>Contact</h1>, handle: { title: 'Contact - EstiMotor' } },         
            ]

        },
    ]);

    return (
        <RouterProvider router={router} />
    )
}
