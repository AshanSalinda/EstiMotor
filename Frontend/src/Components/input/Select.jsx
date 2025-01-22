import React, { useEffect, useState } from 'react';
import Select from 'react-select';
import InputLabel from '@mui/material/InputLabel';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import resolveConfig from "tailwindcss/resolveConfig";
import tailwindConfig from "/tailwind.config.js";

const colors = resolveConfig(tailwindConfig).theme.colors;

const styles = {
    control: (styles, { isFocused, hasValue }) => ({
        ...styles,
        backgroundColor: colors.black,
        height: '3.5rem',
        boxShadow: "none",
        borderRadius: '5px',
        border: hasValue || isFocused ? 'none' : '1px solid #FFFFFFA0',
        '@media (min-width: 768px)': {
            height: '3rem',
        },
        ':hover': {
            border: hasValue || isFocused ? 'none' : '2px solid #FFFFFF90',
        },
    }),
    singleValue: (styles) => ({
        ...styles,
        color: colors.gray[300],
        textAlign: 'left',
        paddingLeft: '3px'
    }),
    menu: (styles) => ({
        ...styles,
        backgroundColor: colors.dark[300],
        zIndex: "2"
    }),
    option: (styles, { isSelected }) => ({
        ...styles,
        textAlign: 'left',
        padding: '10px 15px',
        fontSize: '18px',
        color: 'white',
        backgroundColor: isSelected ? colors.primary[500] : 'transparent',
        ':hover': {
            backgroundColor: isSelected ? colors.primary[500] : '#3a3a3a',
        },
    }),
    input: (styles) => ({ 
        ...styles,
        color: colors.gray[300]
    }),
};

function SelectInput({label, name, isLoading, options = [], onChange}) {
    const [isLabelShrink, setIsLabelShrink] = useState(false);
    const [selected, setSelected] = useState(null);

    const handleLabelShrink = (e) => {
        setIsLabelShrink(e.type === 'focus');
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
                filled={isLabelShrink || !!selected?.value} >
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

            <input type="hidden" name={name} value={selected?.value || ''} />

            <fieldset className={`absolute rounded-[5px] pointer-events-none border-[#FFFFFFA0] w-full ${(isLabelShrink || !!selected?.value) && 'border -top-2 h-16 md:h-14'}`}>
                <legend className={`px-1 ml-[10px] text-xs opacity-0 text-start ${(!isLabelShrink && !selected?.value) && 'hidden'}`} >{label}</legend>
            </fieldset>

        </FormControl>
    )
}

export default SelectInput