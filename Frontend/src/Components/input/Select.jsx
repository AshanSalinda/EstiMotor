import React, { useEffect, useState } from 'react';
import Select from 'react-select';
import InputLabel from '@mui/material/InputLabel';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import styles from '../../theme/reactSelectTheme';


function SelectInput({label, name, isLoading, helperText, options = [], onChange}) {
    const [ isFocused, setIsFocused ] = useState(false);
    const [ selected, setSelected ] = useState(null);

    const handleLabelShrink = (e) => {
        setIsFocused(e.type === 'focus');
    }


    const handleChange = (option) => {
        setSelected(option);

        if (typeof(onChange) === 'function') {
            onChange(option);
        }
    }

    useEffect(() => {
        if (options.length === 1){
            setSelected(options[0]);
        } else if(options.length === 0){
            setSelected(null);
        }
    }, [options]);
    

    return (
        <FormControl className='relative'>
            <InputLabel
                filled={isFocused || !!selected?.value} >
                {label}
            </InputLabel>

            <Select
                options={options}
                styles={styles}
                placeholder={false}
                isClearable
                blurInputOnSelect
                isLoading={isLoading}
                value={selected}
                onFocus={e => handleLabelShrink(e)}
                onBlur={e => handleLabelShrink(e)}
                onChange={option => handleChange(option)}
            />

            <FormHelperText>{helperText || " "}</FormHelperText>

            <input type="hidden" name={name} value={selected?.value || ''} />

            <fieldset className={`absolute rounded-[5px] pointer-events-none w-full ${(isFocused || !!selected?.value) ? '-top-2 h-16 md:h-14' : 'h-14 md:h-12'} ${isFocused ? 'border-2 border-neutral-300' : 'border border-neutral-500'} `}>
                <legend className={`px-1 ml-[10px] text-xs opacity-0 text-start ${(!isFocused && !selected?.value) && 'hidden'}`} >{label}</legend>
            </fieldset>

        </FormControl>
    )
}

export default SelectInput