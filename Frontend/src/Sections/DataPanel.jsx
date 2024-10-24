import React from 'react';

export default function DataPanel({ data }) {
    return (
        <div className='sticky top-0 flex flex-col w-3/5'>
            <div className='w-full rounded h-9 bg-dark-500'/>
            <div className='flex flex-col w-full h-full overflow-y-auto bg-dark-800 overscroll-contain'>
                {(data || []).map((item, index) => (
                    <p className='ml-2' key={index}>{ item }</p>
                ))}
            </div>
        </div>
    )
}
