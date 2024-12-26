import React, { useState } from 'react';
import Input from '../../components/input/Input';
import Button from '../../components/input/Button';

function InputSection() {
    const [displayValue, setDisplayValue] = React.useState(0);

    const handleSubmit = (e) => {
        e.preventDefault();
    
        const element = document.getElementById('display-value');
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });

        const finalValue = 455000;
        const steps = 25;
        const endSpeed = 200;
        const increment = finalValue / steps;

        let currentValue = 0;
        let currentStep = 0;
    
        element.classList.remove('opacity-0', 'animate-glow');
        element.classList.add('animate-fadeIn');
    
        const animateCount = () => {
            const progress = currentStep / steps;
            const currentInterval = endSpeed * progress * progress;

            setTimeout(() => {
                currentValue += increment;
                currentStep++;
        
                if (currentStep < steps) {
                    setDisplayValue(Math.round(currentValue));
                    animateCount();
                } else {
                    setDisplayValue(finalValue);
                    element.classList.add('animate-glow');
                    element.classList.remove('animate-fadeIn');
                }
            }, currentInterval);
        };
    
        animateCount();
    };
    
    
    return (
        <div className='flex min-h-[100vh] flex-col items-center justify-center' id='input-section'>
            <form onSubmit={handleSubmit} className='flex flex-col items-center space-y-16'>
                <h1 className='px-8 text-2xl font-medium text-justify md:text-3xl'>Know Your Vehicle's Market Value Instantly</h1>

                <div className="grid grid-cols-1 gap-5 md:grid-cols-2 md:gap-4">
                    <Input type="text" label="Input 1" />
                    <Input type="text" label="Input 2" />
                    <Input type="text" label="Input 3" />
                    <Input type="text" label="Input 4" />
                    <Input type="text" label="Input 5" />
                    <Input type="text" label="Input 6" />
                    <Input type="text" label="Input 7" />
                    <Input type="text" label="Input 8" />
                    <Input type="text" label="Input 9" />
                </div>

                <Button
                    label="Get Value"
                    size="medium"
                    type="submit"
                    sx={{ width: "10rem", borderRadius: "1.3rem" }}
                />

                <p id='display-value' className="text-4xl font-medium tracking-wide opacity-0">
                    {`LKR ${displayValue.toLocaleString('en-US', { maximumFractionDigits: 2, minimumFractionDigits: 2 })}`}
                </p>
            </form>

        </div>
    )
}

export default InputSection