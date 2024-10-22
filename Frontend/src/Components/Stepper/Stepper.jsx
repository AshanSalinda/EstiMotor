import { useState } from 'react';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import StepContent from '@mui/material/StepContent';

const steps = [
    {
      label: 'Select campaign settings',
      description: `For each ad campaign that you create, you can control how much
                you're willing to spend on clicks and conversions, which networks
                and geographical locations you want your ads to show on, and more.`,
    },
    {
      label: 'Create an ad group',
      description:
        'An ad group contains one or more ads which target a shared set of keywords.',
    },
    {
      label: 'Create an ad',
      description: `Try out different ad text to see what brings in the most customers,
                and learn how to enhance your ads using features like ad extensions.
                If you run into any problems with your ads, find out how to tell if
                they're running and how to resolve approval issues.`,
    },
  ];


  export default function Stepper1() {
    const [activeStep, setActiveStep] = useState(0);
  
    const handleNext = () => {
      setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };
  
    const handleBack = () => {
      setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };
  
    const handleReset = () => {
      setActiveStep(0);
    };
  
    return (
      <div className='max-w-96'>
        <Stepper activeStep={activeStep} orientation="vertical">
          {steps.map((step, index) => (
            <Step key={step.label}>
              <StepLabel
                optional={
                  index === steps.length - 1 ? (
                    <span >Last step</span>
                  ) : <span >A Step</span>
                }
              >
                {step.label}
              </StepLabel>
              <StepContent>
                <span>{step.description}</span>
                <div className='mb-2'>
                  <button
                    onClick={handleNext}
                    className='mt-1 mr-1'
                  >
                    {index === steps.length - 1 ? 'Finish' : 'Continue'}
                  </button>
                  <button
                    disabled={index === 0}
                    onClick={handleBack}
                    className='mt-1 mr-1'
                  >
                    Back
                  </button>
                </div>
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </div>
    );
  }