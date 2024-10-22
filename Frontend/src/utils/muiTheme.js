import { createTheme } from "@mui/material/styles";
import resolveConfig from "tailwindcss/resolveConfig";
import tailwindConfig from "/tailwind.config.js";

const fullConfig = resolveConfig(tailwindConfig);
const colors = fullConfig.theme.colors;
const font = fullConfig.theme.fontFamily.sans.join(",");
const stepperStyles = {
    MuiStepIcon: {
        styleOverrides: {
            root: { fontSize: "30px" },
        },
    },
    MuiStepConnector: {
        styleOverrides: {
            root: { marginLeft: "15px" },
        },
    },
    MuiStepContent: {
        styleOverrides: {
            root: { marginLeft: "15px" },
        },
    },
    MuiStepLabel: {
        styleOverrides: {
            label: { fontSize: "20px" },
        },
    },
}



const muiTheme = createTheme({
    palette: {
        primary: { main: colors.primary[500] },
        secondary: { main: colors.primary[900] },
        text: { primary: "#FFFFFF", secondary: "#FFFFFF", disabled: "#FFFFFF" },
        grey: { 400: "#ff0000" },
    },
    typography: {
        fontFamily: font,
    },
    components: {
        ...stepperStyles,
    },
});

export default muiTheme;
