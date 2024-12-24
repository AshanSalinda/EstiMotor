import { createTheme } from "@mui/material/styles";
import resolveConfig from "tailwindcss/resolveConfig";
import tailwindConfig from "/tailwind.config.js";


const fullConfig = resolveConfig(tailwindConfig);
const colors = fullConfig.theme.colors;
const font = fullConfig.theme.fontFamily.sans.join(",");
const stepperStyles = {
    MuiStepIcon: {
        styleOverrides: {
            root: {
                fontSize: "30px",
                color: colors.dark[200],
                '&.Mui-completed': { color: "#00FF00" },
                '&.Mui-error': { color: '#FF0000' },
            },
        },
    },
    MuiStepConnector: {
        styleOverrides: {
            root: { marginLeft: "15px"},
            line: { borderColor: colors.dark[200] },
        },
    },
    MuiStepContent: {
        styleOverrides: {
            root: { marginLeft: "15px", borderColor: colors.dark[200] },
        },
    },
    MuiStepLabel: {
        styleOverrides: {
            label: { fontSize: "20px", color: '#FFFFFF' },
        },
    },
};

const muiTheme = createTheme({
    palette: {
        primary: { main: colors.primary[500] },
        secondary: { main: colors.primary[900] },
        text: { primary: "#FFFFFF", secondary: 'yellow', disabled: 'orange' },
        grey: { 400: "#ff0000" },
    },
    typography: {
        fontFamily: font,
    },
    components: {
        ...stepperStyles,
        MuiLinearProgress: {
            styleOverrides: {
                root: { borderRadius: "3px" },
                bar: { transition: "none" }
            }
        },
        MuiOutlinedInput: {
            styleOverrides: {
                root: {
                    backgroundColor: colors.black,
                    color: colors.gray[300],
                    borderRadius: "5px",
                    width: "20rem",
                    height: "3rem",

                    '& .MuiOutlinedInput-notchedOutline': {
                        borderWidth: "1px",
                        borderColor: "#FFFFFFA0",
                    },

                    '&:hover .MuiOutlinedInput-notchedOutline': {
                        borderWidth: "2px",
                        borderColor: "#FFFFFF90",
                    },

                    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                        borderColor: "white",
                    },
                },
                notchedOutline: {
                    borderWidth: "2px",
                },
                input: {
                    '&:-webkit-autofill': {
                        // WebkitBoxShadow: '0 0 0 100px #121212 inset',
                        WebkitTextFillColor: colors.gray[300],
                        transition: 'background-color 5000s ease-in-out 0s',
                    },
                  },
            },
        },
        MuiInputLabel: {
            styleOverrides: {
                root: { 
                    color: colors.gray[400],
                    transform: "translate(14px, 13px) scale(1)",

                    '&.MuiFormLabel-filled, &.Mui-focused': { 
                        color: colors.white,
                        transform: "translate(14px, -9px) scale(0.75)"
                    },
                },
            },
        },
    },
});

export default muiTheme;