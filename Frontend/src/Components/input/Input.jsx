import React from 'react';
import OutlinedInput from '@mui/material/TextField';

function input(props) {
    return (
        <OutlinedInput
            size='small'
            {...props}
        />
    )
}

export default input