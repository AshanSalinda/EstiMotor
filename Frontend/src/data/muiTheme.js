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
    },
});

export default muiTheme;
