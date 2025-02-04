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
                    <Content>{ content }</Content>
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


const Content = ({ children }) => {
    return (
        <div className='box-border p-4 rounded bg-dark-400'>
            <table>
                <tbody>
                    <tr>
                        <td>Status:</td>
                        <td>Completed</td>
                    </tr>
                    <tr>
                        <td>Time Taken:</td>
                        <td>1m 30s</td>
                    </tr>
                    <tr>
                        <td>Sent Requests:</td>
                        <td>50</td>
                    </tr>
                    <tr>
                        <td>Field Requests:</td>
                        <td>50</td>
                    </tr>
                    <tr>
                        <td>Success Responses:</td>
                        <td>50</td>
                    </tr>
                    <tr>
                        <td>Errors Responses:</td>
                        <td>0</td>
                    </tr>
                    <tr>
                        <td>Success Rate:</td>
                        <td>100%</td>
                    </tr>

                </tbody>
            </table>
        </div>
    );
}

