import React, { useState, useEffect } from 'react'
import { Step, StepButton, StepContent, Stepper as MuiStepper } from "@mui/material";


export default function MyStepper({ steps, activeStep }) {
    const [expanded, setExpanded] = useState(0)
    const handleClick = (index) => { setExpanded(index); };
    useEffect(() => { setExpanded(activeStep) }, [activeStep])

    return (
        <div className="max-w-96">
            <MuiStepper activeStep={activeStep} orientation="vertical">
            {(steps || []).map((step, index) => (
                <Step key={index}  expanded={expanded == index}>
                    <StepButton onClick={() => handleClick(index)} icon={null} >{step.label}</StepButton>
                    <StepContent>{ expanded == index && step.content }</StepContent>
                </Step>
            ))}
            </MuiStepper>
        </div>
    );
}
