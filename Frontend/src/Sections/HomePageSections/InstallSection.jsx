import { useState, useEffect } from 'react';

export default function InstallationSection() {
    const [deferredPrompt, setDeferredPrompt] = useState(null);

    useEffect(() => {
        const handleBeforeInstallPrompt = (event) => {
            event.preventDefault();
            setDeferredPrompt(event);
        };

        window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

        return () => {
            window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
        };
    }, []);

    const handleInstallClick = () => {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    setDeferredPrompt(null);
                }
            });
        }
    };

    return (
        <div className="p-8 text-center text-white rounded-md shadow-lg ">
            <h2 className="text-2xl font-bold">Install Our App for a Better Experience!</h2>
            <p className="mt-4">Enjoy easy access to all features of EstiMotor on your home screen.</p>
            <div className='flex justify-center mt-6 space-x-4'>
                <div className='relative w-[60vw] h-[40vw]'>
                    <img src="/screenshot-1.png" alt="Desktop App" className='absolute left-0 w-4/6' />
                    <img src="/screenshot-2.png" alt="Desktop App" className='absolute right-0 w-1/6 top-16' />
                </div>
            </div>
            <button
                onClick={handleInstallClick}
                className="px-4 py-2 mt-6 transition duration-300 rounded-lg shadow-lg bg-primary-500 hover:bg-blue-100"
            >
                {!deferredPrompt ? "App Installed" : "Install Now"}
            </button>
        </div>
    )
}
