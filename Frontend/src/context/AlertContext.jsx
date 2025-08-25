import { createContext, useContext, useState } from "react";
import { Snackbar, Alert } from "@mui/material";

const AlertContext = createContext();

export const AlertProvider = ({ children }) => {
    const [alert, setAlert] = useState({
        open: false,
        message: "",
        severity: "success", // success | error | warning | info
    });

    const showAlert = (message, severity = "success") => {
        if (typeof(message) === 'string' && message.trim()) {
            setAlert({ open: true, message, severity });
        }

        // Special handler for API Call Errors
        else if (severity === "apiError") {
            const errorMessage = message?.response?.data?.message || message?.message;
            if (typeof(errorMessage) === 'string' && errorMessage.trim()) {
                setAlert({ open: true, message: errorMessage, severity: "error" });
            }
            console.error(errorMessage);
        }
    };

    const handleClose = () => {
        setAlert(prev => ({ ...prev, open: false }));
    };

    return (
        <AlertContext.Provider value={{ showAlert }}>
            {children}
            <Snackbar
                open={alert.open}
                autoHideDuration={3000}
                onClose={handleClose}
                anchorOrigin={{ vertical: "top", horizontal: "center" }}
            >
                <Alert onClose={handleClose} severity={alert.severity} sx={{ width: "100%" }}>
                    {alert.message}
                </Alert>
            </Snackbar>
        </AlertContext.Provider>
    );
};

export const useAlert = () => useContext(AlertContext);
