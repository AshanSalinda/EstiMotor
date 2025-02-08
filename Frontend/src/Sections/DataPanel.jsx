import { useState } from 'react';
import Button from '../components/input/Button';
import { startTraining, stopTraining } from '../api/modelTrainingApi';

export default function DataPanel({ logs, isRunning, setIsRunning, handleNext}) {
    const [ isStarted, setIsStarted ] = useState(false);

    const handleStart = async () => {
        await startTraining();
        setIsRunning(true);
    };

    const handleStop = async () => {
        await stopTraining();
        setIsRunning(false);
    };  

    return (
        <div className='sticky top-0 flex flex-col w-3/5'>
            <div className='flex w-full gap-10 p-2 rounded bg-dark-400'>
                <Button 
                    label={isRunning ? 'Stop' : 'Start'}
                    size="small"
                    onClick={isRunning ? handleStop : handleStart}
                    sx={{ borderRadius: "1.3rem", fontSize: "1.1rem", padding: "0.1rem 1.5rem" }}
                />

                <Button 
                    label={'Next'}
                    size="small"
                    onClick={handleNext}
                    sx={{ borderRadius: "1.3rem", fontSize: "1.1rem", padding: "0.1rem 1.5rem" }}
                />
            </div>
            
            <div className='flex flex-col w-full h-full overflow-y-auto bg-dark-800 overscroll-contain'>
                {(logs || []).map((item) => (
                    <a href={item} target='_blank' key={item} className='ml-2 text-neutral-300 hover:underline'>{ item }</a>
                ))}
            </div>
        </div>
    )
}
