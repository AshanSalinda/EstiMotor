import { useState } from "react";
import { Step, StepButton, StepLabel, StepContent, Stepper as MuiStepper } from "@mui/material";


const steps = [
    {
        label: "Select campaign settings",
        description: `For each ad campaign that you create, you can control how much
            you're willing to spend on clicks and conversions, which networks
            and geographical locations you want your ads to show on, and more.`,
    },
    {
        label: "Create an ad group",
        description:
            "An ad group contains one or more ads which target a shared set of keywords.",
    },
    {
        label: "Create an ad",
        description: `Try out different ad text to see what brings in the most customers,
                and learn how to enhance your ads using features like ad extensions.
                If you run into any problems with your ads, find out how to tell if
                they're running and how to resolve approval issues.`,
    },
];

export default function MyStepper() {
    const [activeStep, setActiveStep] = useState(0);
    const [expanded, setExpanded] = useState(0)


    const handleNext = (index) => {
        setActiveStep(index + 1);
        setExpanded(index + 1);
    };

    const handleClick = (index) => {
        setExpanded(index);
    };

    const handleReset = () => {
        setActiveStep(0);
    };

    return (
        <div className="max-w-96">
            <MuiStepper activeStep={activeStep} orientation="vertical">
                {(steps || []).map((step, index) => (
                    <Step key={index}  expanded={expanded == index}>
                        <StepButton onClick={() => handleClick(index)} >{step.label}</StepButton>
                        <StepContent>
                            { expanded == index && (
                            <Content onNext={handleNext} index={index}>
                                {step.description}
                            </Content>
                            )}
                        </StepContent>
                    </Step>
                ))}
            </MuiStepper>
        </div>
    );
}


function Content({ onNext, index, children }) {
    return (
        <div>
            <div>{children}</div>
            <div>
                <button
                    onClick={() => onNext(index)}
                    disabled={false}
                    className="px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700"
                >
                    Next
                </button>
            </div>
        </div>
    );
}
