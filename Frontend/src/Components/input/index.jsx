import { forwardRef } from 'react';
import BaseInput from './BaseInput'
import NumberInput from './NumberInput'

const Index = forwardRef((props, ref) => {
    if (props.type === 'number') return <NumberInput {...props} ref={ref} />
    return <BaseInput {...props} ref={ref} />
});

export default Index