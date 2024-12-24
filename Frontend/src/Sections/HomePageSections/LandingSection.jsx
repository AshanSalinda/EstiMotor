import React from 'react';
import logo from '../../assets/logo.svg';
import car from '../../assets/white_car.png';

function LandingSection() {
    const handleClick = () => {
        document.getElementById('input-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    return (
        // <div className='w-full min-h-[100vh] py-8 flex items-center justify-between relative bg-[url(src/assets/background.jpeg)] bg-cover bg-no-repeat bg-center'>
        <div className='w-full min-h-[100vh] py-8 flex items-center'>
            <div className='px-10 space-y-10 md:px-20 lg:px-32'>
                <img src={logo} alt="EstiMotor" className='w-44 md:w-48 drop-shadow-[#000000] mx-auto md:mx-0' />
                <h1 className='text-3xl md:text-[2.6rem] leading-tight font-semibold drop-shadow-2xl'>Accelerate with<br />Confident Pricing</h1>
                <p className='text-lg max-w-[30rem] font-light text-[#E0E0E0]'>Our AI-driven platform brings transparency to the used vehicle market by providing accurate price predictions for your vehicle.</p>
                <button
                    onClick={handleClick}
                    className="px-4 py-2 bg-blue-500 rounded w-fit hover:bg-blue-700" >
                    Try it now
                </button>
            </div>

            <div className='absolute right-0 z-[-1]'>
                <img src={car} alt="Car" />
            </div>
        </div>
    )
}

export default LandingSection