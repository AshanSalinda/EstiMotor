import { forwardRef } from 'react';
import PropTypes from 'prop-types';
import OutlinedInput from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';

const Input = forwardRef(({ ending, helperText, ...rest }, ref) => {
    return (
        <OutlinedInput
            size='large'
            inputRef={ref}
            helperText={helperText || " "}
            {...rest}
            slotProps={{
                input: {
                    endAdornment: ending && <InputAdornment position="end">{ ending }</InputAdornment>
                },
            }}
        />
    );
});

Input.propTypes = {
    ending: PropTypes.node || PropTypes.string,
    helperText: PropTypes.string,
};

export default Input