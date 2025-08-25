import React from 'react';
import { LinearProgress } from "@mui/material";


export default function ProgressBar({ progress }) {
    return (
        <div className=''>
            { progress < 0 ?
                <LinearProgress className='mt-2' variant="indeterminate" aria-label="Step Progress Bar" /> :
                <LinearProgress className='mt-2' variant="determinate" value={progress} aria-label="Step Progress Bar" />
            }
            <span className='block w-full text-sm font-medium text-right text-gray-400'>{progress < 0 ? " " : progress + '%'}</span>
        </div>
    );
}
