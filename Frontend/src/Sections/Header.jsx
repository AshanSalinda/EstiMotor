import React from "react";
import Logo from "/EstiMotor.svg";

export default function Header({ title }) {
    return (
        <div className="relative flex items-center justify-center w-screen h-12 px-2 bg-stone-800">
            <img src={Logo} alt="EstiMotor" className="absolute w-24 h-auto left-2"/>
            <h1 className="text-2xl font-bold text-white">{ title }</h1>
        </div>
    );
}
