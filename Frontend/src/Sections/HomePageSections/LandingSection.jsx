import React from 'react';
import Button from '../../components/input/Button';

function LandingSection() {
    const handleClick = () => {
        document.getElementById('input-section').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    return (
        <div className='relative flex flex-col w-full min-h-screen onlyMd:min-h-fit'>

            {/* Background */}
            <div className='absolute bg-gradient-to-t from-black to-transparent from-[40%] bg-[0%_100%] animate-gradientMove z-[-1] w-full min-h-full h-screen' style={{backgroundSize: "100% 200%"}}></div>
            <img src="/home-background.webp" alt="Background" className='absolute object-cover w-full min-h-full h-screen z-[-2] brightness-110 contrast-100 md:brightness-125'/>

            {/* Logo */}
            <img src="/logo.svg" alt="EstiMotor" className='w-40 pt-20 mx-auto lg:mx-32 md:w-44 text-shadow' />

            {/* Content */}
            <div className='px-10 py-16 mt-3 md:mt-10 lg:mt-5 space-y-14 md:px-20 lg:px-32'>
                <h1 className='text-[9vw] leading-snug md:text-[3rem] md:leading-[3.75rem] font-semibold text-shadow'>Accelerate with<br />Confident Pricing</h1>
                <p className='text-base md:text-lg text-justify md:max-w-[30rem] font-light text-[#E0E0E0] text-shadow'>Our AI-driven platform brings transparency to the used vehicle market by providing accurate price predictions for your vehicle.</p>
                
                <Button
                    onClick={handleClick}
                    label="Try It Now"
                    size="large"
                    outlined
                    sx={{width: "8.5rem"}}
                />

            </div>
        </div>
    )
}

export default LandingSection