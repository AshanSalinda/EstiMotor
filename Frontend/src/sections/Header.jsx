import React from "react";
import { MdCloudSync } from "react-icons/md";
import { FaUsersGear } from "react-icons/fa6";
import { Link, useLocation } from "react-router-dom";
import PropTypes from "prop-types";
import Tooltip from '@mui/material/Tooltip';

export default function Header({ title }) {
    const { pathname } = useLocation();

    return (
        <div className="relative flex items-center justify-center h-[8vh] px-2 bg-dark-350">

            <Link to="/" className="absolute left-2">
                <img src="/logo.svg" alt="EstiMotor" className="w-20 h-auto"/>
            </Link>

            <h1 className="text-xl font-medium leading-tight text-dark-100 max-w-36 md:max-w-none text-center">
                { title || "EstiMotor" }
            </h1>

            <div className="absolute flex items-center space-x-4 text-3xl text-neutral-400 right-8">
                <Tooltip title="Model Training" arrow>
                    <Link to="/model-training">
                        <MdCloudSync className={pathname === '/model-training' ? 'text-primary-500' : 'text-neutral-400'} />
                    </Link>
                </Tooltip>

                <Tooltip title="Admin Managements" arrow>
                    <Link to="/admin-management">
                        <FaUsersGear className={pathname === '/admin-management' ? 'text-primary-500' : 'text-neutral-400'} />
                    </Link>
                </Tooltip>
            </div>
        </div>
    );
}

Header.propTypes = {
    title: PropTypes.string,
    buttonLabel: PropTypes.string,
    onClick: PropTypes.func,
}
