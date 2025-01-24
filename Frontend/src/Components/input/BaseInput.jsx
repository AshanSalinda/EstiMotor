import { forwardRef } from 'react';
import OutlinedInput from '@mui/material/TextField';

const Input = forwardRef(({ unit, helperText, ...rest }, ref) => {
    return (
        <OutlinedInput
            size='large'
            inputRef={ref}
            helperText={helperText || " "}
            {...rest}
        />
    );
});

export default Input