import React from 'react';
import Input from '../../components/input/Input';

function InputSection() {
  return (
    <div className='flex min-h-[100vh] flex-col items-center' id='input-section'>
        <h1 className='px-8 text-2xl font-medium text-justify lg:mt-32'>Know Your Vehicle's Market Value Instantly</h1>

        <div className="grid grid-cols-1 gap-5 mt-16 md:gap-4 md:grid-cols-2">
            <Input type="text" label="Input 1" />
            <Input type="text" label="Input 2" />
            <Input type="text" label="Input 3" />
            <Input type="text" label="Input 4" />
            <Input type="text" label="Input 5" />
            <Input type="text" label="Input 6" />
            <Input type="text" label="Input 7" />
            <Input type="text" label="Input 8" />
            <Input type="text" label="Input 9" />
        </div>

    </div>
  )
}

export default InputSection