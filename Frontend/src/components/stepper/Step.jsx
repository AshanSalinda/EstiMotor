import React from 'react';
import { StepLabel, StepContent, Collapse } from "@mui/material";
import { useStepDataContext } from '../../context/StepDataContext';
import ProgressBar from "../ProgressBar.jsx";


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

const Content = ({ content }) => {
    return (
        <div className='box-border p-4 rounded-md bg-dark-400'>
            <table>
                <tbody>
                    {
                        (typeof content === 'object')
                        ?
                        Object.keys(content).map((key) =>
                            <tr key={key}>
                                <td className='pr-4'>{key}:</td>
                                <td className='w-20'>{content[key]}</td>
                            </tr>
                        )
                        :
                        <tr>
                            <td className='w-52'>{content}</td>
                        </tr>
                    }
                </tbody>
            </table>
        </div>
    );
}
