import React, { useState, useEffect } from 'react'
import { 
    Collapse, 
    Step, 
    StepLabel,
    StepContent, 
    Stepper as MuiStepper 
} from "@mui/material";


export default function MyStepper({ steps, activeStep }) {
    const [expanded, setExpanded] = useState(0)

    const handleClick = (index) => {
        if(index > activeStep) return;
        setExpanded(index); 
    };

    useEffect(() => { 
        setExpanded(activeStep) 
    }, [activeStep])

    return (
        <div className="max-w-96">
            <MuiStepper activeStep={activeStep} orientation="vertical">
                {(steps || []).map((step, index) => (

                    <Step key={index}  expanded={expanded == index} >
                        <StepLabel 
                            error={step.error} 
                            className={index <= activeStep ? 'cursor-pointer' : 'cursor-default'} 
                            onClick={() => handleClick(index)} icon={null}
                            optional={activeStep === index && <div className='w-full h-1 bg-primary-500'></div>} >
                            {step.title}
                        </StepLabel>

                        <StepContent >
                            <Collapse 
                                in={expanded === index} 
                                timeout="auto" 
                                unmountOnExit >
                                { step.content }
                            </Collapse>
                        </StepContent>
                    </Step>
                ))}
            </MuiStepper>
        </div>
    );
}
