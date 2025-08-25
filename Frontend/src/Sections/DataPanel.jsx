import Button from '../components/input/Button';

export default function DataPanel({ logs, isRunning, handleRunning, handleNext}) { 

    return (
        <div className='sticky top-0 flex flex-col w-3/5'>
            <div className='flex w-full gap-10 p-2 rounded bg-dark-400'>
                <Button 
                    label={isRunning ? 'Stop' : 'Start'}
                    color={isRunning ? 'secondary' : 'primary'}
                    size="small"
                    onClick={handleRunning}
                    sx={{ width: "8rem", borderRadius: "1.3rem", fontSize: "1.1rem", padding: "0.1rem 1.5rem" }}
                />

                <Button 
                    label={'Next'}
                    size="small"
                    onClick={handleNext}
                    sx={{ width: "8rem", borderRadius: "1.3rem", fontSize: "1.1rem", padding: "0.1rem 1.5rem" }}
                />
            </div>
            
            <div className='flex flex-col w-full h-full overflow-y-auto scrollable bg-dark-800 overscroll-contain'>
                {(logs || []).map((item) => (
                    <a href={item} target='_blank' key={item} className='ml-2 text-neutral-300 hover:underline'>{ item }</a>
                ))}
            </div>
        </div>
    )
}
