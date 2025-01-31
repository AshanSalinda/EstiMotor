import LandingSection from '../sections/HomePageSections/LandingSection';
import InputSection from '../sections/HomePageSections/InputSection';
import InstallSection from '../sections/HomePageSections/InstallSection';
import Footer from '../sections/HomePageSections/Footer';

function HomePage() {
    return (
        <div>
            <LandingSection />
            <InputSection />
            <InstallSection />
            <Footer />
        </div>
    )
}

export default HomePage