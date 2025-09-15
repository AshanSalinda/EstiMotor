import React from 'react';
import { Button as MuiButton } from '@mui/material';

function Button({ label, outlined, ...rest }) {
    const variant = outlined ? "outlined" : "contained";

    return (
        <MuiButton variant={variant} {...rest} >{label}</MuiButton>
    )
}

export default Button