import React from 'react';
import logo from '../../assets/logo.svg';
import background1 from '../../assets/white_car.png';
import background from '../../assets/home_background.webp';
import Button from '../../components/input/Button';

function LandingSection() {
    const handleClick = () => {
        document.getElementById('input-section').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    return (
        <div className='relative flex flex-col w-full min-h-screen'>

            {/* Background */}
            <div className='absolute bg-gradient-to-t from-black to-transparent from-[40%] bg-[0%_0%] animate-gradientMove z-[-1] w-full h-full' style={{backgroundSize: "100% 200%"}}></div>
            <img src={background} alt="Background" className='absolute object-cover w-full h-full z-[-2] brightness-110'/>
            {/* <img src={background1} alt="Background" className='absolute right-0 z-[-1]' /> */}

            {/* Logo */}
            <img src={logo} alt="EstiMotor" className='w-40 pt-20 mx-auto lg:mx-32 md:w-44 text-shadow' />

            {/* Content */}
            <div className='px-10 py-16 mt-3 md:mt-10 lg:mt-5 space-y-14 md:px-20 lg:px-32'>
                <h1 className='text-[2rem] leading-tight md:text-[3rem] md:leading-[3.5rem] font-semibold text-shadow'>Accelerate with<br />Confident Pricing</h1>
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