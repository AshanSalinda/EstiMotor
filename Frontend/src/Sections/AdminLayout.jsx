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
        <div>
            <Header title={title} />
            <div className="flex h-[92vh]">
                <SideNavbar />
                <div className="flex flex-col flex-grow h-full overflow-y-auto bg-dark-700">
                    <Outlet />
                </div>
            </div>
        </div>
    );
}