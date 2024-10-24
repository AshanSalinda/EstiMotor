import React, { useState, useEffect } from 'react';
import { StepLabel, StepContent, Collapse } from "@mui/material";

const Step = ({ index, title, content, isActive, isExpanded, setLogs }) => {
    const [isFailed, setIsFailed] = useState(false);

    const startProcessing = async () => {
        setLogs(`${title} is starting...`);
        await new Promise(resolve => setTimeout(resolve, 2000));

        setLogs(`Processing...`);
        await new Promise(resolve => setTimeout(resolve, 2000));

        setIsFailed(true);
        setLogs(`${title} Error occurred...`);
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        setIsFailed(false);
        setLogs(`${title} Completed...`);
    }

    useEffect(() => {
        if(isActive) startProcessing();
    }, [isActive])


    return (
        <>
            <StepLabel 
                optional={isActive && <div className='w-full h-1 bg-primary-500'></div>}
                error={isFailed}>
                {title}
            </StepLabel>
            <StepContent>
                <Collapse 
                    in={isExpanded} 
                    timeout="auto" 
                    unmountOnExit >
                    { content }
                </Collapse>
            </StepContent>
        </>
    );
}

export default Step;
