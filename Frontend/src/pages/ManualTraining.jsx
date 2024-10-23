import React, { useState } from 'react'
import Stepper from '../components/Stepper/Stepper';

const steps = [
    {
        label: "Web Scraping",
        content: `For each ad campaign that you create, you can control how much
            you're willing to spend on clicks and conversions, which networks
            and geographical locations you want your ads to show on, and more.`,
    },
    {
        label: "Data Cleaning",
        content:
            "An ad group contains one or more ads which target a shared set of keywords.",
    },
    {
        label: "Data Transformation",
        content: `Try out different ad text to see what brings in the most customers,
                and learn how to enhance your ads using features like ad extensions.
                If you run into any problems with your ads, find out how to tell if
                they're running and how to resolve approval issues.`,
    },
    {
        label: "Model Training",
        content: `Try out different ad text to see what brings in the most customers,
                and learn how to enhance your ads using features like ad extensions.
                If you run into any problems with your ads, find out how to tell if
                they're running and how to resolve approval issues.`,
    },
    {
        label: "Completed",
        content: `Try out different ad text to see what brings in the most customers,
                and learn how to enhance your ads using features like ad extensions.
                If you run into any problems with your ads, find out how to tell if
                they're running and how to resolve approval issues.`,
    },
];


export default function ManualTraining() {
    const [activeStep, setActiveStep] = useState(0);

    return (
        <div>
            <Stepper steps={steps} activeStep={activeStep}/>
            <button 
                onClick={() => setActiveStep(pre => (pre + 1) % steps.length)} 
                className="px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700" >
                Next
            </button>
        </div>
        
        
    )
}
