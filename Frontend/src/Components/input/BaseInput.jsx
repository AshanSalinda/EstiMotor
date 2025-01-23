import React from 'react';
import OutlinedInput from '@mui/material/TextField';

function input({ unit, helperText, ...rest }) {
    return (
        <OutlinedInput
            size='large'
            helperText={helperText || " "}
            {...rest}
            // slotProps={{
            //     input: {
            //         endAdornment: <InputAdornment position="end">Km</InputAdornment>
            //     },
            // }}
        />
    )
}

export default input