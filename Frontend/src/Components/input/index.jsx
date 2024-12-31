import React from 'react'
import BaseInput from './BaseInput'
import NumberInput from './NumberInput'

function Index(props) {
    if (props.type === 'number') return <NumberInput {...props} />
    return <BaseInput {...props} />
}

export default Index