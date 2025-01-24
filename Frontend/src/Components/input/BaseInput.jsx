import { forwardRef } from 'react';
import PropTypes from 'prop-types';
import OutlinedInput from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';

const Input = forwardRef(({ unit, helperText, ...rest }, ref) => {
    return (
        <OutlinedInput
            size='large'
            inputRef={ref}
            helperText={helperText || " "}
            {...rest}
            slotProps={{
                input: {
                    endAdornment: unit && <InputAdornment position="end">{ unit }</InputAdornment>
                },
            }}
        />
    );
});

Input.propTypes = {
    unit: PropTypes.string,
    helperText: PropTypes.string,
};

export default Input