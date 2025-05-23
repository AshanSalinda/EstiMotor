import { useState, useEffect, useRef } from 'react';
import { startTraining, stopTraining } from '../api/modelTrainingApi';
import { stepsInfo } from '../data/steps.json';
import { all } from 'axios';

export default function useStepData() {
    const [progress, setProgress] = useState(0);
    const [activeStep, setActiveStep] = useState(0);
    const [expandedStep, setExpandedStep] = useState(0);
    const [expandedStepLogs, setExpandedStepLogs] = useState([]);
    const [expandedStepStats, setExpandedStepStats] = useState({});
    const [isFailed, setIsFailed] = useState(false);
    const [isRunning, setIsRunning] = useState(false);
    const allLogs = useRef(stepsInfo.map(() => []));
    const allStepStats = useRef(stepsInfo.map(() => ({
        'Status': "Pending",
        'Time Taken': "00:00:00",
        'Success Rate': "0%",
        'Request Count': 0,
        'Success Count': 0,
        'Failure Count': 0,
    })));

    const setLogs = (payload) => {
        const newProgress = payload?.progress;
        const newStats = payload?.stats;
        const newLogs = payload?.logs?.reverse();
        const newControl = payload?.control;

        if(newProgress) {
            setProgress(newProgress);
        }

        if(newStats) {
            allStepStats.current[activeStep] = newStats;

            if (activeStep === expandedStep) {
                setExpandedStepStats(newStats);
            }
        }

        if(newLogs) {
            allLogs.current[activeStep].unshift(...newLogs);

            if (activeStep === expandedStep) {
                setExpandedStepLogs([...allLogs.current[activeStep]]);
            }
            
        }

        if(newControl) {
            if(newControl === 'completed') {
                handleNext();

                if (activeStep === 1) {
                    setIsRunning(false);
                }
            }
        }

    };

    const handleNext = () => {
        const nextStep = activeStep < 0 ? 0 : (activeStep + 1) % stepsInfo.length;

        setExpandedStep(nextStep);
        setActiveStep(nextStep);
        setProgress(0);
    };

    const handleRunning = () => {
        if(isRunning) {
            stopTraining().then(() => setIsRunning(false));
        } else {
            startTraining().then(() => {
                setIsRunning(true)
                setActiveStep(0);
                setExpandedStep(0);
                setProgress(0);
                allLogs.current = stepsInfo.map(() => []);
                allStepStats.current = stepsInfo.map(() => ({
                    'Status': "Pending",
                    'Time Taken': "00:00:00",
                    'Success Rate': "0%",
                    'Request Count': 0,
                    'Success Count': 0,
                    'Failure Count': 0,
                }));
            });
        }
    };


    useEffect(() => {
        setExpandedStepLogs(allLogs.current[expandedStep]);
        setExpandedStepStats(allStepStats.current[expandedStep]);
    }, [expandedStep]);


    return {
        stepsInfo,
        isFailed,
        progress,
        activeStep,
        expandedStep,
        stepStats: expandedStepStats,
        logs: expandedStepLogs,
        isRunning,
        handleRunning,
        setLogs,
        setActiveStep,
        setExpandedStep,
        handleNext,
    };
}
