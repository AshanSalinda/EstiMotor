import React from "react";
import { MdCloudSync } from "react-icons/md";
import { FaUsersGear } from "react-icons/fa6";
import { Link, useLocation } from "react-router-dom";
import PropTypes from "prop-types";

export default function Header({ title, buttonLabel, onClick }) {
    const { pathname } = useLocation();

    return (
        <div className="relative flex items-center justify-center h-[8vh] px-2 bg-dark-300">
            <img src="/logo.svg" alt="EstiMotor" className="absolute w-20 h-auto left-2"/>

            <div className="absolute flex items-center space-x-4 text-2xl text-neutral-400 left-36">
                <Link to="/model-training">
                    <MdCloudSync className={pathname === '/model-training' ? 'text-primary-500' : 'text-neutral-400'} />
                </Link>

                <Link to="/admin-details">
                    <FaUsersGear className={pathname === '/admin-details' ? 'text-primary-500' : 'text-neutral-400'} />
                </Link>
            </div>

            <h1 className="text-xl font-normal text-dark-100">{ title || "EstiMotor" }</h1>

            { typeof(onClick) === "function" &&
            <button 
                onClick={onClick} 
                className="absolute px-4 py-2 bg-blue-500 rounded right-2 w-fit hover:bg-blue-700" >
                { buttonLabel || "Next" }
            </button>
            }
        </div>
    );
}

Header.propTypes = {
    title: PropTypes.string,
    buttonLabel: PropTypes.string,
    onClick: PropTypes.func,
}
