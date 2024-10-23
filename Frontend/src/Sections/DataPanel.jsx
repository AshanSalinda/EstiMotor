import React from 'react';

export default function DataPanel({data}) {
  return (
    <div className='sticky top-0 flex flex-col w-3/5'>
        <div className='w-full rounded h-9 bg-dark-400'></div>
        <div className='flex flex-col-reverse w-full h-full overflow-y-auto bg-dark-700 overscroll-contain'>
            {data.map((d, i) => (
                <div key={i} className='flex items-center justify-between h-16 px-4 border-b border-dark-600'>
                    <div>{d.name}</div>
                    <div className='flex items-center'>
                        <button className='px-2 py-1 text-white bg-red-500 rounded hover:bg-red-700'>Delete</button>
                    </div>
                </div>
            ))}
        </div>
    </div>
  )
}
