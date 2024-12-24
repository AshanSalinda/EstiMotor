import React from 'react';
import AdminLayout from '../sections/AdminLayout';
import Stepper from '../components/Stepper/Stepper';
import DataPanel from '../sections/DataPanel';
import useWebSocket from '../hooks/useWebSocket';
import StepDataProvider, { useStepDataContext } from '../context/StepDataContext';


function ModelTraining() {
    const { logs, handleNext } = useStepDataContext();
    useWebSocket();


    return (
        <AdminLayout title="Model Training" onClick={handleNext}>
            <div className='flex justify-between h-full mx-8 my-4 overflow-y-auto'>
                <Stepper />
                <DataPanel data={logs}/>
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
