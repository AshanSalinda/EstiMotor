import LandingSection from '../sections/HomePageSections/LandingSection';
import ValuationSection from '../Sections/HomePageSections/ValuationSection.jsx';
import InstallSection from '../sections/HomePageSections/InstallSection';
import Footer from '../sections/HomePageSections/Footer';

function HomePage() {
    return (
        <div>
            <LandingSection />
            <ValuationSection />
            <InstallSection />
            <Footer />
        </div>
    )
}

export default HomePage