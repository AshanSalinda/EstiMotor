import React, { useState } from 'react';
import Input from '../../components/input/Input';
import Button from '../../components/input/Button';
import useDisplayValueAnimation from '../../hooks/useDisplayValueAnimation';
import { getPrediction } from '../../api/userApi';

function InputSection() {
    const [ isLoading, setIsLoading ] = useState(false);
    const { displayValue, animateCount } = useDisplayValueAnimation();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
    
        const element = document.getElementById('display-value');
        element.classList.add('opacity-0');
        
        if(element.getBoundingClientRect().bottom >= window.innerHeight){
            element.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }

        const vehicleValue = await getPrediction();
        setIsLoading(false);

        element.classList.remove('opacity-0', 'animate-glow');
        element.classList.add('animate-fadeIn');
        
        await animateCount(vehicleValue);
        
        element.classList.add('animate-glow');
        element.classList.remove('animate-fadeIn');
    };
    
    
    return (
        <div id='input-section' className='flex justify-center min-h-screen mb-40 md:-mt-52 lg:mt-28 onlyMd:min-h-fit'>
            <form onSubmit={handleSubmit} className='flex flex-col items-center justify-center -mb-10 space-y-16'>
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


                <div className='relative'>
                    { isLoading &&                    
                        <div className="absolute flex items-center justify-center w-full h-10 space-x-2">
                            <div className="w-3 h-3 bg-gray-500 rounded-full animate-[bounce_1.5s_ease-in-out_infinite]"></div>
                            <div className="w-3 h-3 bg-gray-500 rounded-full animate-[bounce_1.5s_ease-in-out_200ms_infinite]"></div>
                            <div className="w-3 h-3 bg-gray-500 rounded-full animate-[bounce_1.5s_ease-in-out_400ms_infinite]"></div>
                        </div>
                    }
                    
                    <p id='display-value' className="pb-10 text-3xl font-medium tracking-tight opacity-0 text-slate-100 md:text-4xl tabular-nums font-monoSpace">
                        {`LKR ${displayValue}`}
                    </p>
                </div>

            </form>
        </div>
    )
}

export default InputSection