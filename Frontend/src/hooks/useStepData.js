import { useState, useEffect, useRef } from 'react';
import { startTraining, stopTraining } from '../api/modelTrainingApi';
import { useAlert } from "../context/AlertContext.jsx";
import { stepsInfo } from '../data/steps.json';
import useWebSocket from "./useWebSocket.js";


export default function useStepData() {
    const [isLoading, setIsLoading] = useState(false);
    const [isWsConnected, setIsWsConnected] = useState(false);
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
        'Duration': "00:00:00"
    })));

    const { showAlert } = useAlert();

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
        const step_count = stepsInfo.length;
        // If model training step is completed, mark the next step also as completed
        if (activeStep === step_count - 2) {
            allStepStats.current[step_count - 1] = {'Model Training Completed': ''}
            setExpandedStep(step_count - 1);
            setActiveStep(step_count);
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
