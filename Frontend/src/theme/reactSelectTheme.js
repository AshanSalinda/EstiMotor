import resolveConfig from "tailwindcss/resolveConfig";
import tailwindConfig from "../../tailwind.config.js";

const colors = resolveConfig(tailwindConfig).theme.colors;

const styles = {
    control: (styles, { isFocused, hasValue }) => ({
        ...styles,
        backgroundColor: colors.black,
        height: '3.5rem',
        boxShadow: "none",
        borderRadius: '5px',
        border: '2px solid transparent',	
        '@media (min-width: 768px)': {
            height: '3rem',
        },
        ':hover': {
            borderColor: hasValue || isFocused ? 'transparent' : '#737373',
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
    dropdownIndicator: (styles) => ({
        ...styles,
        color: colors.neutral[300],
        ':hover': {
            color: colors.neutral[400],
        },
    }),
    indicatorSeparator: (styles) => ({
        ...styles,
        backgroundColor: colors.neutral[600],
    }),
};

export default styles;