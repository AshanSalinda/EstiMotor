import React, { useState } from 'react'
import Stepper from '../components/Stepper/Stepper';
import DataPanel from '../sections/DataPanel';

const steps = [
    {
        label: "Data Collecting",
        description: "Gather vehicle data from multiple sources",
        content: "Gather vehicle data from multiple sources, including websites and user inputs.",
    },
    {
        label: "Data Cleaning",
        description: "Process and clean the collected data",
        content: "Process and clean the collected data to ensure accuracy and consistency.",
    },
    {
        label: "Data Transformation",
        description: "Transform the data into a structured format",
        content: "Transform the cleaned data into a structured format suitable for model training.",
    },
    {
        label: "Model Training",
        description: "Train the machine learning model",
        content: "Train the machine learning model using the transformed data to predict vehicle prices.",
    },
    {
        label: "Completed",
        content: "The model is ready and predictions can now be made for vehicle price estimation.",
    },
];



export default function ManualTraining() {
    const [activeStep, setActiveStep] = useState(0);
    const [data, setData] = useState([]);

    return (
        <div className='flex justify-between h-full mx-8 my-4 overflow-y-auto'>
            <div className='w-96'>
                <Stepper steps={steps} activeStep={activeStep}/>
                <button 
                    onClick={() => setActiveStep(pre => (pre + 1) % steps.length)} 
                    className="px-4 py-2 bg-blue-500 rounded hover:bg-blue-700" >
                    Next
                </button>
                <button 
                    onClick={() => setData(pre => [{name: 'data ' + pre.length}, ...pre])} 
                    className="px-4 py-2 bg-blue-500 rounded hover:bg-blue-700" >
                    Add
                </button>
            </div>
            <DataPanel data={data}/>
        </div>  
    )
}
