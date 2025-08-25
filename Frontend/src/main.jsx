import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { AlertProvider } from "./context/AlertContext.jsx";
import MuiThemeProvider from "./context/MuiThemeContext.jsx";
import Routes from "./routes/Routes.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <MuiThemeProvider>
            <AlertProvider>
                <Routes />
            </AlertProvider>
        </MuiThemeProvider>
    </StrictMode>
);