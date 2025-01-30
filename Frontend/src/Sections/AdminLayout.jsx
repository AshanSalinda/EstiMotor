import React from "react";
import PropTypes from "prop-types";
import Header from "./Header";
import SideNavbar from "./SideNavbar";

export default function AdminLayout(props) {
    const { children, ...headerProps } = props;

    return (
        <div>
            <Header {...headerProps} />
            <div className="flex h-[92vh]">
                <SideNavbar />
                <div className="flex flex-col flex-grow h-full overflow-y-auto bg-dark-700">
                    { children }
                </div>
            </div>
        </div>
    );
}

AdminLayout.propTypes = {
    children: PropTypes.node,
}