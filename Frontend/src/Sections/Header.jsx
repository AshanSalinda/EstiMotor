import React from "react";
import logo from "../assets/logo.svg";

export default function Header({ title, buttonText, onClick }) {
    return (
        <div className="relative flex items-center justify-center h-[8vh] px-2 bg-dark-300">
            <img src={logo} alt="EstiMotor" className="absolute w-20 h-auto left-2"/>
            <h1 className="text-xl font-normal text-dark-100">{ title || "EstiMotor" }</h1>

            { typeof(onClick) === "function" &&
            <button 
                onClick={onClick} 
                className="absolute px-4 py-2 bg-blue-500 rounded right-2 w-fit hover:bg-blue-700" >
                { buttonText || "Next" }
            </button>
            }
        </div>
    );
}
