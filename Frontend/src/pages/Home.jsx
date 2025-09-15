import LandingSection from '../sections/homePageSections/LandingSection';
import ValuationSection from '../sections/homePageSections/ValuationSection.jsx';
import InstallSection from '../sections/homePageSections/InstallSection';
import Footer from '../sections/homePageSections/Footer';

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