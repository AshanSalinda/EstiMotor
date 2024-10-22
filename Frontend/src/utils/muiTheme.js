import { createTheme } from '@mui/material/styles';
import resolveConfig from 'tailwindcss/resolveConfig';
import tailwindConfig from '/tailwind.config.js';

const fullConfig = resolveConfig(tailwindConfig);
const colors = fullConfig.theme.colors
const font = fullConfig.theme.fontFamily.sans.join(',')

const muiTheme = createTheme({
    palette: {
        primary: { main: colors.primary[500] },
        secondary: { main: colors.primary[900] },
        grey: { 400: '#ff0000' }
      },
      typography: {
        fontFamily: font,
      },
})

export default muiTheme;