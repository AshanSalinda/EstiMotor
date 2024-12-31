import React, { useState } from 'react';
import Input from '../../components/input';
import Button from '../../components/input/Button';
import Select from '../../components/input/Select'
import useDisplayValueAnimation from '../../hooks/useDisplayValueAnimation';
import { getPrediction } from '../../api/userApi';

function InputSection() {
    const [ isLoading, setIsLoading ] = useState(false);
    const { displayValue, animateCount } = useDisplayValueAnimation();

    const options = [
        { value: 'chocolate', label: 'Chocolate' },
        { value: 'strawberry', label: 'Strawberry' },
        { value: 'vanilla', label: 'Vanilla' }
    ]

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
        <div id='input-section' className='flex justify-center min-h-screen px-2 mb-40 md:px-10 md:-mt-52 lg:mt-28 onlyMd:min-h-fit'>
            <form onSubmit={handleSubmit} className='flex lg:min-w-[48vw] flex-col items-center justify-center space-y-16 text-center bg-gradient-to-tl from-[#0b0b0b] to-[#171717] border border-slate-900 rounded-2xl md:rounded-3xl md:px-16 lg:px-16'>

                <h1 className='px-10 pt-20 text-3xl font-semibold text-gray-200 max-w-[32rem] md:text-3xl'>Know Your Vehicle's Market Value Instantly</h1>

                <div className="grid w-[85vw] md:w-fit grid-cols-1 gap-6 md:grid-cols-2 md:gap-4 lg:min-w-[34rem]">
                    <Select name="Make" label="Manufacturer" options={options} />
                    <Select name="Model" label="Model" options={options} />
                    <Select name="Year" label="Make Year" options={options} />
                    <Select name="Transmission" label="Transmission" options={options} />
                    <Select name="Fuel type" label="Fuel type" options={options} />
                    <Input type="text" label="Engine capacity" prefix="CC" autoComplete='off' />
                    <Input type="number" label="Mileage" prefix="Km " autoComplete='off' />
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
                    
                    <p id='display-value' className="pb-16 text-3xl font-medium tracking-tight opacity-0 text-slate-100 md:text-4xl tabular-nums font-monoSpace">
                        {`LKR ${displayValue}`}
                    </p>
                </div>

            </form>
        </div>
    )
}

export default InputSection