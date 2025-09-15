import AdminLayout from '../sections/AdminLayout';
import Stepper from '../components/stepper/Stepper';
import DataPanel from '../sections/DataPanel';
import StepDataProvider, { useStepDataContext } from '../context/StepDataContext';


function ModelTraining() {
    const { logs, isRunning, isLoading, handleRunning, handleNext } = useStepDataContext();

    return (
        <AdminLayout title="Model Training" isLoading={isLoading} >
            <div className='flex justify-between h-full px-8 py-4 min-w-[960px] overflow-y-auto scrollable'>
                <Stepper />
                <DataPanel {...{logs, isRunning, handleRunning, handleNext}}/>
            </div>  
        </AdminLayout>
    )
}


export default function WrappedModelTraining() {
    return (
        <StepDataProvider>
            <ModelTraining />
        </StepDataProvider>
    );
}
