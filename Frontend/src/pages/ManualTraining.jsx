import React, { useState } from 'react'
import Stepper from '../components/Stepper/Stepper';
import DataPanel from '../sections/DataPanel';
import { stepsInfo } from '../utils/steps.json';


export default function ManualTraining() {
    const [activeStep, setActiveStep] = useState(0);
    const [steps, setSteps] = useState(stepsInfo);
    const [data, setData] = useState([]);

    const markAsError = () => {
        steps[activeStep].error = true;
        setSteps([...steps]);
    }

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
                    onClick={() => markAsError()} 
                    className="px-4 py-2 bg-blue-500 rounded hover:bg-blue-700" >
                    Error
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
