import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider } from '@mui/material/styles';
import muiTheme from "./utils/muiTheme.js";
import Routes from "./Routes.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
    <StrictMode>
        <ThemeProvider theme={muiTheme}>
            <Routes />
        </ThemeProvider>
    </StrictMode>
);