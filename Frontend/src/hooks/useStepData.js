import { useState, useEffect, useRef } from 'react';
import { stepsInfo } from '../data/steps.json';

export default function useStepData() {
    const [progress, setProgress] = useState(0);
    const [activeStep, setActiveStep] = useState(0);
    const [expandedStep, setExpandedStep] = useState(0);
    const [expandedStepLogs, setExpandedStepLogs] = useState([]);
    const [isFailed, setIsFailed] = useState(false);
    const allLogs = useRef(stepsInfo.map(() => []));

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
    };


    useEffect(() => {
        setExpandedStepLogs(allLogs.current[expandedStep]);
    }, [expandedStep]);


    return {
        stepsInfo,
        isFailed,
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
