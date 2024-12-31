import React, { useState } from 'react';
import BaseInput from './BaseInput';

function NumberInput({ prefix, onBlur, ...props }) {
    const [ value, setValue ] = useState('');

    const getFormattedValue = (value, key = '') => {
        const numericValue = parseFloat(value.replace(new RegExp(`^${prefix}`), '').replace(/,/g, '') + key);

        if (isNaN(numericValue)) return '';

        return (prefix+ "" + numericValue.toLocaleString('en-US', {
            maximumFractionDigits: 10
        }));
    }

    const handleChange = (e) => {
        const key = e.key;

        if (key === '.') {
            setValue(prev => !prev.includes('.') ? (prev || 0) + key : prev);
            return;
        }

        if (key === 'Backspace') {
            setValue(prev => {
                const cursorPosition = e.target.selectionStart;
                
                if (prefix && cursorPosition <= prefix?.length) {
                    return '';
                }
    
                return prev.slice(0, cursorPosition - 1) + prev.slice(cursorPosition);
            });
            
            return;
        }

        if (key !== ' ' && !isNaN(key)) {
            setValue(prev => getFormattedValue(prev, key));
        }
    }

    onblur = () => {
        setValue(prev => getFormattedValue(prev));
        console.log("Blur");
        if (onBlur) onBlur();
    }
    
    return (
        <BaseInput {...props} value={value} onKeyDown={handleChange} onBlur={onBlur} type="text" />
    )
}

export default NumberInput