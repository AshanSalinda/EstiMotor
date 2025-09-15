import { useEffect, useState, forwardRef } from 'react';
import Select from 'react-select';
import InputLabel from '@mui/material/InputLabel';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import styles from '../../theme/reactSelectTheme';


const SelectInput = forwardRef((props, ref) => {
    const [isFocused, setIsFocused] = useState(false);
    const [isHovered, setIsHovered] = useState(false);
    const [selected, setSelected] = useState(null);
    

    const { 
        options = [],
        isFullOptionRequired = false,
        label, 
        id, 
        name, 
        isLoading, 
        helperText, 
        error, 
        onChange, 
        onBlur 
    } = props;


    const getBorderStyles = () => {
        if (isFocused) return "border-2 border-neutral-300";
        if (isHovered) return "border-2 border-neutral-500";
        if (error) return "border border-red-600";
        return "border border-neutral-500";
    }


    const handleChange = (option, e, b) => {
        setSelected(option);

        if (typeof (onChange) === 'function') {
            onChange({
                target: {
                    value: isFullOptionRequired ? option : option?.value,
                    name: name
                },
            });
        }
    }


    const handleBlur = (e) => {
        setIsFocused(false);

        if (typeof (onBlur) === 'function') {
            onBlur(e);
        }
    }


    useEffect(() => {
        if (options.length === 1) {
            handleChange(options[0]);
        } else if (selected && !options.find(opt => opt.value === selected.value)) {
            handleChange(null);
        }
    }, [options]);


    useEffect(() => {
        const element = document.getElementById(id);

        if (!element) return;

        element.addEventListener('mouseenter', () => setIsHovered(true));
        element.addEventListener('mouseleave', () => setIsHovered(false));

        return () => {
            element.removeEventListener('mouseenter', () => setIsHovered(true));
            element.removeEventListener('mouseleave', () => setIsHovered(false));
        };
    }, [])


    return (
        <FormControl className='relative'>
            <InputLabel
                filled={isFocused || !!selected?.value}
                htmlFor={`${id}-select-input`} >
                {label}
            </InputLabel>

            <Select
                id={id}
                inputId={`${id}-select-input`}
                ref={ref}
                name={name}
                options={options}
                styles={styles}
                placeholder={false}
                isClearable
                blurInputOnSelect
                menuPortalTarget={document.body}
                menuShouldScrollIntoView={true}
                isLoading={isLoading}
                value={selected}
                aria-invalid={error}
                onFocus={e => setIsFocused(true)}
                onBlur={e => handleBlur(e)}
                onChange={(option, e, b) => handleChange(option, e, b)}
            />

            <FormHelperText error={error} >{helperText || " "}</FormHelperText>


            <fieldset className={`absolute rounded-[5px] pointer-events-none w-full ${(isFocused || !!selected?.value) ? '-top-2 h-16 md:h-14' : 'h-14 md:h-12'} ${getBorderStyles()}` }>
                <legend className={`px-1 ml-[9px] text-xs opacity-0 text-start ${(!isFocused && !selected?.value) && 'hidden'}`} >{label}</legend>
            </fieldset>

        </FormControl>
    )
});

export default SelectInput;