import React from 'react';
import OutlinedInput from '@mui/material/TextField';

function input({ unit, ...rest }) {
    return (
        <OutlinedInput
            size='large'
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