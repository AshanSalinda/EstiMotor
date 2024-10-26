import React, { createContext, useContext } from 'react';
import useStepData from '../hooks/useStepData';

const StepDataContext = createContext();

const StepDataProvider = ({ children }) => {
    const stepData = useStepData();
    return (
        <StepDataContext.Provider value={stepData}>
            {children}
        </StepDataContext.Provider>
    );
};

export const useStepDataContext = () => useContext(StepDataContext);

export default StepDataProvider;