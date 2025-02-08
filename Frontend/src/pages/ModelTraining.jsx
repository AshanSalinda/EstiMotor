import React from 'react';
import AdminLayout from '../sections/AdminLayout';
import Stepper from '../components/Stepper/Stepper';
import DataPanel from '../sections/DataPanel';
import useWebSocket from '../hooks/useWebSocket';
import StepDataProvider, { useStepDataContext } from '../context/StepDataContext';


function ModelTraining() {
    const { logs, isRunning, setIsRunning, handleNext } = useStepDataContext();
    useWebSocket();


    return (
        <AdminLayout title="Model Training" >
            <div className='flex justify-between h-full px-8 py-4 min-w-[960px] overflow-y-auto'>
                <Stepper />
                <DataPanel {...{logs, isRunning, setIsRunning, handleNext}}/>
            </div>  
        </AdminLayout>
    )
}


export default function WrappedManualTraining() {
    return (
        <StepDataProvider>
            <ModelTraining />
        </StepDataProvider>
    );
}
