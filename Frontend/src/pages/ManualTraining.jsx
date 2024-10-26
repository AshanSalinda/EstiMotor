import React from 'react'
import Stepper from '../components/Stepper/Stepper';
import DataPanel from '../sections/DataPanel';
import useWebSocket from '../hooks/useWebSocket';
import StepDataProvider, { useStepDataContext } from '../context/StepDataContext';


function ManualTraining() {
    useWebSocket();
    const { logs, handleNext } = useStepDataContext();


    return (
        <>
            <button 
                onClick={handleNext} 
                className="px-4 py-2 ml-auto mr-10 bg-blue-500 rounded w-fit hover:bg-blue-700" >
                Next
            </button>
            <div className='flex justify-between h-full mx-8 my-4 overflow-y-auto'>
                <Stepper />
                <DataPanel data={logs}/>
            </div>  
        </>
    )
}


export default function WrappedManualTraining() {
    return (
        <StepDataProvider>
            <ManualTraining />
        </StepDataProvider>
    );
}
