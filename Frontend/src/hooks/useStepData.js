import { useState, useEffect, useRef } from 'react';
import { stepsInfo } from '../data/steps.json';

export default function useStepData() {
    const [progress, setProgress] = useState(0);
    const [activeStep, setActiveStep] = useState(-1);
    const [expandedStep, setExpandedStep] = useState(-1);
    const [expandedStepLogs, setExpandedStepLogs] = useState([]);
    const allLogs = useRef({ 0: [], 1: [], 2: [], 3: [], 4: [] });

    const setLogs = (payload) => {
        const newProgress = payload?.progress;
        const newLogs = payload?.logs?.reverse();

        if(newProgress) {
            setProgress(newProgress);
        }

        if(newLogs) {
            allLogs.current[activeStep].unshift(...newLogs);

            if (activeStep === expandedStep) {
                setExpandedStepLogs([...allLogs.current[activeStep]]);
            }
        }

    };

    const handleNext = () => {
        const nextStep = activeStep < 0 ? 0 : (activeStep + 1) % stepsInfo.length;

        setExpandedStep(nextStep);
        setActiveStep(nextStep);
        setExpandedStepLogs([]);
    };

    useEffect(() => {
        setExpandedStepLogs(allLogs.current[expandedStep] || []);
    }, [expandedStep]);


    return {
        stepsInfo,
        progress,
        activeStep,
        expandedStep,
        logs: expandedStepLogs,
        setLogs,
        setActiveStep,
        setExpandedStep,
        handleNext,
    };
}
