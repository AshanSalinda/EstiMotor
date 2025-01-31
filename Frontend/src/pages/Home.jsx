import { useState, useEffect } from 'react';
import LandingSection from '../sections/HomePageSections/LandingSection';
import InputSection from '../sections/HomePageSections/InputSection';
import Footer from '../sections/HomePageSections/Footer';

function HomePage() {
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
        <div>
            <LandingSection />
            <InputSection />
            <button onClick={handleInstallClick} className='p-8 text-white bg-primary-500'>{!deferredPrompt ? "App Installed" : "Install App"}</button>
            <Footer />
        </div>
    )
}

export default HomePage