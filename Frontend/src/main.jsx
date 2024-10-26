import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import MuiThemeProvider from "./context/MuiThemeContext.jsx";
import StepDataProvider from "./context/StepDataContext.jsx";
import Routes from "./Routes.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <MuiThemeProvider>
            <Routes />
        </MuiThemeProvider>
    </StrictMode>
);