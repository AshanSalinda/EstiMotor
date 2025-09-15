import ProgressBar from "../components/ProgressBar.jsx";


export default function LoadingPage() {
    return (
        <div className="bg-black h-screen w-screen flex items-center justify-center">
            <div className="flex flex-col items-center gap-6">
                <img
                    src="/logo.svg"
                    alt="Logo"
                    width="200px"
                    height="auto"
                    className="block"
                />
                <div className="w-64">
                    <ProgressBar progress={-1} />
                </div>
            </div>
        </div>
    );
}
