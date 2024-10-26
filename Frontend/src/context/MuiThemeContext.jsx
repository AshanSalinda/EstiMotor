import { ThemeProvider } from '@mui/material/styles';
import muiTheme from "../data/muiTheme";

const MuiThemeProvider = ({ children }) => {
    return (
        <ThemeProvider theme={muiTheme}>
            {children}
        </ThemeProvider>
    );
};

export default MuiThemeProvider;