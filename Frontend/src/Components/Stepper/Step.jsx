import React, { useState, useEffect } from 'react';
import { StepLabel, StepContent, Collapse } from "@mui/material";

const Step = ({ title, content, isActive, isExpanded }) => {
    const [isFailed, setIsFailed] = useState(false);

    const startProcessing = async () => {
        await new Promise(resolve => setTimeout(resolve, 2000));

        setIsFailed(true);
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        setIsFailed(false);
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
