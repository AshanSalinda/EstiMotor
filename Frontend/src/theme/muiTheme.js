import { createTheme } from "@mui/material/styles";
import resolveConfig from "tailwindcss/resolveConfig";
import tailwindConfig from "../../tailwind.config.js";


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
            root: { marginLeft: "15px" },
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

const inputStyles = {
    MuiOutlinedInput: {
        styleOverrides: {
            root: {
                backgroundColor: colors.black,
                color: colors.gray[300],
                borderRadius: "5px",
                width: "100%",

                '@media (min-width: 768px)': {
                    height: '3rem'
                },

                '& .MuiOutlinedInput-notchedOutline': {
                    borderWidth: "1px",
                    borderColor: colors.neutral[500],
                },

                '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderWidth: "2px",
                    borderColor: colors.neutral[500],
                },

                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: colors.neutral[300],
                },
            },
            notchedOutline: {
                borderWidth: "2px",
            },
            input: {
                '&:-webkit-autofill': {
                    WebkitTextFillColor: colors.gray[300],
                    transition: 'background-color 5000s ease-in-out 0s',
                },
            },
        },
    },
    MuiFormHelperText: {
        styleOverrides: {
            root: {
                marginLeft: '5px',

                '&.Mui-error': {
                    color: colors.red[600],
                },
            },
        },
    },
    MuiInputLabel: {
        styleOverrides: {
            root: {
                color: colors.gray[400],
                userSelect: "none",
                transform: "translate(14px, 17px) scale(1)",

                '&.Mui-error': {
                    color: colors.gray[400],
                },

                '@media (min-width: 768px)': {
                    transform: "translate(14px, 12px) scale(1)"
                },

                '&.MuiFormLabel-filled, &.Mui-focused': {
                    color: colors.white,
                    transform: "translate(14px, -8px) scale(0.75)"
                },
            },
        },
    },
    MuiInputAdornment: {
        styleOverrides: {
          root: {
            color: colors.neutral[300],
            fontWeight: '500',
          },
        },
    },
    MuiTypography: {
        styleOverrides: {
            root: {
                color: 'inherit',
                fontWeight: 'inherit',
            },
        },
    },
};


const muiTheme = createTheme({
    palette: {
        primary: { main: colors.primary[500] },
        secondary: { main: colors.primary[900] },
        error: { main: colors.red[600] },
        text: { primary: "#FFFFFF", secondary: 'yellow', disabled: 'orange' },
        grey: { 400: "#ff0000" },
    },
    typography: {
        fontFamily: font,
    },
    components: {
        ...stepperStyles,
        ...inputStyles,

        MuiLinearProgress: {
            styleOverrides: {
                root: { borderRadius: "3px" },
                bar: { transition: "none" }
            }
        },
        MuiFormControl: {
            styleOverrides: {
                root: { width: "100%" }
            }
        },
        MuiSnackbar: {
            styleOverrides: {
                root: {
                }
            }
        },
        MuiAlert: {
            styleOverrides: {
                root: {
                    boxShadow: "0 2px 6px rgba(0,0,0,0.3)",
                },
                standard: {
                    '&.MuiAlert-standardSuccess': {
                        backgroundColor: "#0c400c",
                        color: "#a8e6a3",
                    },
                    '&.MuiAlert-standardInfo': {
                        backgroundColor: "#062438",
                        color: "#80dfff",
                    },
                    '&.MuiAlert-standardWarning': {
                        backgroundColor: "#241a0b",
                        color: "#ffd97d",
                    },
                    '&.MuiAlert-standardError': {
                        backgroundColor: "#480d0d",
                        color: "#f49797",
                    },
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    padding: "0 1.2rem",
                    fontSize: "1.1rem",
                    textTransform: "none",
                    boxShadow: "0 2px 4px 0 #FFFFFF50",
                    '&:hover': { boxShadow: "0 2px 5px 0 #FFFFFF50" }
                },
                contained: {
                    backgroundColor: colors.primary[500],
                    '&:hover': { backgroundColor: "#3AA0FF" },
                    '&.Mui-disabled': {
                        backgroundColor: colors.primary[500],
                        color: "inherit",
                        opacity: "0.4"
                    },
                    '&.MuiButton-colorSecondary': {
                        backgroundColor: colors.red[600],
                        boxShadow: "none",
                        '&:hover': { backgroundColor: colors.red[500] }
                    }
                },
                outlined: {
                    boxShadow: "none",
                    border: "1px solid " + colors.primary[500],
                    backgroundColor: "#00000050",
                    color: colors.primary[450],
                    '&:hover': {
                        boxShadow: "0 1px 4px 0 " + colors.primary[450],
                    },
                },
                sizeMedium: {
                    height: "2.7rem",
                    fontWeight: "400",
                },
                sizeLarge: {
                    height: "2.8rem",
                    fontWeight: "500",
                }
            },
        },
    },
});

export default muiTheme;