import { useState } from 'react';

export default function useDisplayValueAnimation() {
    const [displayValue, setDisplayValue] = useState('');
    const maxDelay = 150;
    let steps = 30;
    let paddingLength = 0;

    const setFormattedDisplayValue = (value) => {
        const formattedValue = value
            .toFixed(2)
            .padStart(paddingLength, '0')
            .replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        
        setDisplayValue(formattedValue);
    }

    const performAnimation = (valueToDisplay, resolve) => {
        const increment = valueToDisplay / steps;
        let currentValue = 0;
        let currentStep = 0;

        const animate = () => {
            const progress = currentStep / steps;
            const easedOutProgress = Math.pow(progress - 0.15, 3);
            const currentInterval = maxDelay * easedOutProgress;

            setTimeout(() => {
                currentValue += increment;
                currentStep++;

                if (currentStep < steps) {
                    setFormattedDisplayValue(currentValue);
                    animate();
                } else {
                    setFormattedDisplayValue(valueToDisplay);
                    resolve();
                }
            }, currentInterval);
        };

        animate();
    };

    const animateCount = (valueToDisplay) => new Promise((resolve) => {
        paddingLength = Math.floor(Math.log10(valueToDisplay)) + 4;
        setFormattedDisplayValue(0);
        
        setTimeout(() => {
            performAnimation(valueToDisplay, resolve);
        }, 1000);
    });

    return { displayValue, animateCount };
}
