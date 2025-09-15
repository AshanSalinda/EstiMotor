import { useState, forwardRef, useEffect } from 'react';
import BaseInput from './BaseInput';

const NumberInput = forwardRef(({onBlur, onChange, ...props}, ref) => {
    const [ value, setValue ] = useState('');

    const getFormattedValue = (value, key = '') => {
        const numericValue = parseFloat(value.replace(/,/g, '') + key);

        if (isNaN(numericValue)) return '';

        return (numericValue.toLocaleString('en-US', {
            maximumFractionDigits: 3
        }));
    }

    const handleCopy = (e) => {
        e.preventDefault();

        const selectedText = window.getSelection().toString();
        const formattedText = selectedText.replace(/,/g, '');
        e.clipboardData.setData('text', formattedText);
    };

    const handlePaste = (e) => {
        e.preventDefault();

        const pastedValue = (e.clipboardData.getData('text')).replace(/,/g, '');
    
        if (!isNaN(pastedValue) || pastedValue.trim() !== '') {
            const cursorStart = e.target.selectionStart;
            const cursorEnd = e.target.selectionEnd;

            setValue(prev => getFormattedValue(
                prev.slice(0, cursorStart) + 
                pastedValue + 
                prev.slice(cursorEnd)
            ));
        }
    };

    const handleKeyDown = (e) => {
        const key = e.nativeEvent.data || e.nativeEvent.inputType;

        if (key === '.') {
            setValue(prev => !prev.includes('.') ? (prev || 0) + key : prev);
            return;
        }

        if (key === "deleteContentBackward") {
            const cursorPosition = e.target.selectionStart + 1;

            if (cursorPosition === 0) return;

            setValue(prev => prev.slice(0, cursorPosition - 1) + prev.slice(cursorPosition));

            setTimeout(() => {
                e.target.selectionStart = cursorPosition - 1;
                e.target.selectionEnd = cursorPosition - 1;
            }, 0);

            return;
        }


        if (key !== ' ' && !isNaN(key)) {
            setValue(prev => getFormattedValue(prev, key));
        }
    }

    const handleBlur = (e) => {
        setValue(prev => getFormattedValue(prev));

        if (typeof(onBlur) === 'function') {
            onBlur(e);
        }
    }

    useEffect(() => {
        if (typeof(onChange) === 'function') {
            onChange({
                target: {
                    value: value.replace(/,/g, ''),
                    name: props.name
                }
            });
        }
    }, [value]);
    
    return (
        <BaseInput 
            {...props} 
            ref={ref} 
            value={value} 
            onInput={handleKeyDown} 
            onCopy={handleCopy}
            onCut={(e) => { handleCopy(e); setValue(''); }}
            onPaste={handlePaste} 
            onBlur={handleBlur} 
            inputMode="decimal"
            type="text"
        />
    )
});

NumberInput.propTypes = BaseInput.propTypes;

export default NumberInput