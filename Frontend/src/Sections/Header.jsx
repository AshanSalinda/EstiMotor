import React from "react";
import Logo from "/Esti.svg";
import New from "/new.svg"
import Imnew from "/emnew.svg"
import EM from "/em.png"

export default function Header({ title }) {
    return (
        <div className="relative flex items-center justify-center w-screen h-12 px-2 bg-dark-300">
            <img src={EM} alt="EstiMotor" className="absolute w-12 h-auto left-2"/>
            {/* <img src={Logo} alt="EstiMotor" className="absolute w-20 h-auto left-2"/>
            <img src={Imnew} alt="EstiMotor" className="absolute w-24 h-auto left-28"/>
            <img src={New} alt="EstiMotor" className="absolute h-auto left-56 w-28"/> */}
            <h1 className="text-xl font-normal text-dark-100">{ title }</h1>
        </div>
    );
}
