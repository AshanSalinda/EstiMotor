import React from 'react';
import { StepLabel, StepContent, Collapse, LinearProgress } from "@mui/material";
import { useStepDataContext } from '../../context/StepDataContext';


const Step = ({ index, title, content, isActive, isExpanded }) => {
    const { progress, isFailed } = useStepDataContext();

    return (
        <>
            <StepLabel 
                optional={ isActive && <ProgressBar progress={progress} /> } 
                error={isFailed[index]}>
                {title}
            </StepLabel>
            <StepContent>
                <Collapse in={isExpanded} timeout="auto" unmountOnExit >{ content }</Collapse>
            </StepContent>
        </>
    );
}


const ProgressBar = ({ progress }) => {
    return (
        // <div className='flex items-center justify-between'>
        //     <LinearProgress className='w-10/12' variant="determinate" value={progress} />
        //     <span className='text-sm font-medium text-gray-400'>{progress + '%'}</span>
        // </div>

        <div className=''>
            <LinearProgress className='mt-2' variant="determinate" value={progress} />
            <span className='block w-full text-sm font-medium text-right text-gray-400'>{progress + '%'}</span>
        </div>
        
    );
}

export default Step;
