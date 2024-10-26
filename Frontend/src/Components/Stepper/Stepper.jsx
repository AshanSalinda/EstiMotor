import React from 'react'
import { Stepper as MuiStepper, Step as MuiStep } from "@mui/material";
import { useStepDataContext } from '../../context/StepDataContext';
import Step from './Step';


export default function MyStepper() {
    const { activeStep, expandedStep, setExpandedStep, stepsInfo } = useStepDataContext();

    const handleClick = (index) => {
        if(index > activeStep) return;
        if(index === expandedStep) return;
        setExpandedStep(index); 
    };


    return (
        <div className="max-w-96">
            <MuiStepper activeStep={activeStep} orientation="vertical">
                { stepsInfo.map((step, index) => (
                    <MuiStep 
                        key={index} 
                        onClick={() => handleClick(index)} 
                        expanded={expandedStep == index}
                        className={index === expandedStep ? 'cursor-default' : 'cursor-pointer'} >

                        <Step
                            index={index}
                            title={step.label} 
                            content={step.content} 
                            isActive={index === activeStep}
                            isExpanded={index === expandedStep}
                        /> 
                    </MuiStep>
                ))}
            </MuiStepper>
        </div>
    );
}
