import React from "react";
import Logo from "/EstiMotor.svg";

export default function Header({ title }) {
    return (
        <div className="relative flex items-center justify-center w-screen px-2 h-14 bg-dark-300">
            <img src={Logo} alt="EstiMotor" className="absolute w-24 h-auto left-2"/>
            <h1 className="text-xl font-normal text-dark-100">{ title }</h1>
        </div>
    );
}
