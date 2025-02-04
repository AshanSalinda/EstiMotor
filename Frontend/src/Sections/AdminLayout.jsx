import React from "react";
import PropTypes from "prop-types";
import Header from "./Header";

export default function AdminLayout(props) {
    const { children, ...headerProps } = props;

    return (
        <div className="flex flex-col h-screen bg-dark-700">
            <Header {...headerProps} />
            <div className="flex-1 overflow-y-auto">
                { children }
            </div>
        </div>
    );
}

AdminLayout.propTypes = {
    children: PropTypes.node,
}