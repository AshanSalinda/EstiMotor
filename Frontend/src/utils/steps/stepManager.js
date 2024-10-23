import { useState } from "react";
import DataCollectingStep from "./DataCollecting";
import DataCleaningStep from "./DataCleaning";
import Step from "./Step";


export default function stepManager ()  {
    const steps = [
        new DataCollectingStep(),
        new DataCleaningStep(),
        new Step("Data Transformation", "Transforming data into the required format..."),
        new Step("Model Training", "Training the machine learning model..."),
        new Step("Completed", "Process has been completed."),
    ];

    const [activeStep, setActiveStep] = useState(0);
    const [logs, setLogs] = useState([]);

    const addLog = (message, logRef) => {
        logRef = [message, ...logRef];
        setLogs(prev => [message, ...prev]);
    };

    const start = async () => {
        for (let i = 0; i < steps.length; i++) {
            const step = steps[i];
            setActiveStep(i);
            await step.start(addLog);  // Start each step asynchronously
        }
    };


    return { steps, activeStep, logs, start };
};
