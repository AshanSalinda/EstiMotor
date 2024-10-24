import React, { useState, useEffect, useRef } from 'react'
import Stepper from '../components/Stepper/Stepper';
import DataPanel from '../sections/DataPanel';
import { stepsInfo } from '../utils/steps.json';


export default function ManualTraining() {
    const [activeStep, setActiveStep] = useState(0);
    const [expandedStep, setExpandedStep] = useState(0);
    const [expandedStepLogs, setExpandedStepLogs] = useState([]);
    const allLogs = useRef({ 0: [], 1: [], 2: [], 3: [], 4: [] });

    const setLogs = (message) => {
        allLogs.current[activeStep].unshift(message);

        if (activeStep === expandedStep) {
            setExpandedStepLogs([...allLogs.current[activeStep]]);
        }
    };

    const handleNext = () => {
        const nextStep = (activeStep + 1) % stepsInfo.length;

        setExpandedStep(nextStep);
        setActiveStep(nextStep);
        setExpandedStepLogs([]);
    };

    useEffect(() => {
        setExpandedStepLogs(allLogs.current[expandedStep] || []);
    }, [expandedStep]);

    return (
        <>
            <button 
                onClick={handleNext} 
                className="px-4 py-2 ml-auto mr-10 bg-blue-500 rounded w-fit hover:bg-blue-700" >
                Next
            </button>
            <div className='flex justify-between h-full mx-8 my-4 overflow-y-auto'>
                <Stepper activeStep={activeStep} expandedStep={expandedStep} setExpandedStep={setExpandedStep} setLogs={setLogs}/>
                <DataPanel data={expandedStepLogs}/>
            </div>  
        </>
    )
}
