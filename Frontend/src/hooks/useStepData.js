import { useState, useEffect, useRef } from 'react';
import { startTraining, stopTraining } from '../api/modelTrainingApi';
import { useAlert } from "../context/AlertContext.jsx";
import { stepsInfo } from '../data/steps.json';
import useWebSocket from "./useWebSocket.js";


export default function useStepData() {
    const [isWsConnected, setIsWsConnected] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isRunning, setIsRunning] = useState(false);
    const [isFailed, setIsFailed] = useState(false);
    const [progress, setProgress] = useState(0);
    const [activeStep, setActiveStep] = useState(0);
    const [expandedStep, setExpandedStep] = useState(0);
    const [expandedStepLogs, setExpandedStepLogs] = useState([]);
    const [expandedStepStats, setExpandedStepStats] = useState({});
    const allLogs = useRef(stepsInfo.map(() => []));
    const allStepStats = useRef(stepsInfo.map(() => ({
        'Status': "Pending",
        'Duration': "00:00:00"
    })));

    const { showAlert } = useAlert();

    const setLogs = (payload) => {
        const newProgress = payload?.progress;
        const newStats = payload?.stats;
        const newLogs = payload?.logs?.reverse();
        const newControl = payload?.control;

        if(newProgress !== undefined && newProgress !== null) {
            setProgress(newProgress);
        }

        if(newStats) {
            const overridden_stats = {
                ...(allStepStats.current[activeStep]),
                ...newStats,
            }

            allStepStats.current[activeStep] = overridden_stats;

            if (activeStep === expandedStep) {
                setExpandedStepStats(overridden_stats);
            }
        }

        if(newLogs) {
            let current_logs = allLogs.current[activeStep] || [];
            current_logs.unshift(...newLogs);              // Add new logs to the beginning
            current_logs = current_logs.slice(0, 100);     // Keep only the latest 100 logs
            allLogs.current[activeStep] = current_logs;

            if (activeStep === expandedStep) {
                setExpandedStepLogs([...allLogs.current[activeStep]]);
            }
            
        }

        if(newControl) {
            switch (newControl) {
                case 'completed':
                    handleNext();
                    break;
                case 'failed':
                    setIsFailed(true);
                    setIsRunning(false);
                    if (progress === -1) {
                        setProgress(0);
                    }
                    break;
            }
        }

    };

    const handleNext = () => {
        const step_count = stepsInfo.length;
        // If model training step is completed, mark the next step also as completed
        if (activeStep === step_count - 2) {
            allStepStats.current[step_count - 1] = `Model Training Completed at: ${new Date().toLocaleTimeString()} on ${new Date().toLocaleDateString()}`;
            setExpandedStep(step_count - 1);
            setActiveStep(step_count);
            setProgress(0);
            setIsRunning(false);
        }
        // If last step is the active step
        else if (activeStep === step_count) {
            allLogs.current = stepsInfo.map(() => [])
            setExpandedStep(0);
            setActiveStep(0);
            setProgress(0);
        }
        else {
            const nextStep = activeStep < 0 ? 0 : (activeStep + 1) % step_count;

            setExpandedStep(nextStep);
            setActiveStep(nextStep);
            setProgress(0);
        }
    };

    const handleRunning = () => {
        setIsLoading(true);

        if(isRunning) {
            stopTraining()
                .then((data) => {
                    showAlert(data?.message);
                    setIsRunning(false);
                })
                .catch(error => showAlert(error, "apiError"))
                .finally(() => setIsLoading(false));
        }

        else {
            if (!isWsConnected) {
                setIsLoading(false);
                showAlert("WS not Connected", "error");
                return
            }
            startTraining()
                .then((data) => {
                    showAlert(data?.message);
                    setIsRunning(true);
                    setIsFailed(false);
                    setActiveStep(0);
                    setExpandedStep(0);
                    setProgress(0);
                    allLogs.current = stepsInfo.map(() => []);
                    allStepStats.current = stepsInfo.map(() => ({
                        'Status': "Pending",
                        'Duration': "00:00:00"
                    }));
                })
                .catch(error => showAlert(error, "apiError"))
                .finally(() => setIsLoading(false));
        }
    };


    useEffect(() => {
        setExpandedStepLogs(allLogs.current[expandedStep]);
        setExpandedStepStats(allStepStats.current[expandedStep]);
    }, [expandedStep]);

    useWebSocket({ isWsConnected, setIsWsConnected, setLogs } )


    return {
        stepsInfo,
        isFailed,
        progress,
        activeStep,
        expandedStep,
        stepStats: expandedStepStats,
        logs: expandedStepLogs,
        isRunning,
        isLoading,
        handleRunning,
        setActiveStep,
        setExpandedStep,
        handleNext,
    };
}
