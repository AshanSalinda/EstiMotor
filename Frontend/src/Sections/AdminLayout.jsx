import React from "react";
import { Outlet, useMatches } from "react-router-dom";
import Header from "./Header";
import SideNavbar from "./SideNavbar";

export default function AdminLayout() {
    const matches = useMatches();
    const title =
        matches.length > 0
            ? matches[matches.length - 1]?.handle?.title || "EstiMotor"
            : "EstiMotor";

    return (
        <div className="flex flex-col w-screen h-screen">
            <Header title={title} />
            <div className="flex flex-grow w-screen">
                <SideNavbar />
                <div className="w-full h-full bg-dark-500">
                    <Outlet />
                </div>
            </div>
        </div>
    );
}
