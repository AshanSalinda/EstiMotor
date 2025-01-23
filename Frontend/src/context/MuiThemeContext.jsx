import { ThemeProvider } from '@mui/material/styles';
import muiTheme from "../theme/muiTheme";

const MuiThemeProvider = ({ children }) => {
    return (
        <ThemeProvider theme={muiTheme}>
            {children}
        </ThemeProvider>
    );
};

export default MuiThemeProvider;