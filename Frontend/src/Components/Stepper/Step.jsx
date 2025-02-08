import React from 'react';
import { StepLabel, StepContent, Collapse, LinearProgress } from "@mui/material";
import { useStepDataContext } from '../../context/StepDataContext';


export default function Step({ title, content, isActive, isExpanded }) {
    const { progress, isFailed } = useStepDataContext();

    return (
        <>
            <StepLabel 
                optional={ isActive && <ProgressBar progress={progress} /> } 
                error={isActive && isFailed}>
                {title}
            </StepLabel>

            <StepContent>
                <Collapse in={isExpanded} timeout="auto" unmountOnExit >
                    <Content content={content} />
                </Collapse>
            </StepContent>
        </>
    );
}


const ProgressBar = ({ progress }) => {
    return (
        <div className=''>
            <LinearProgress className='mt-2' variant="determinate" value={progress} aria-label="Step Progress Bar" />
            <span className='block w-full text-sm font-medium text-right text-gray-400'>{progress + '%'}</span>
        </div>
    );
}


const Content = ({ content }) => {
    return (
        <div className='box-border p-4 rounded-md bg-dark-400'>
            <table>
                <tbody>
                    { Object.keys(content).map((key) => 
                        <tr key={key}>
                            <td className='pr-4'>{key}:</td>
                            <td className='w-20'>{content[key]}</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}

