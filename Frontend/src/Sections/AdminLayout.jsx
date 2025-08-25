import Header from "./Header";
import ProgressBar from "../Components/ProgressBar.jsx";

export default function AdminLayout(props) {
    const { children, isLoading, ...headerProps } = props;

    return (
        <div className="flex flex-col h-screen bg-dark-700">
            <Header {...headerProps} />
            <div className="flex-1 overflow-y-auto scrollable">
                { children }
            </div>

            {/* Loading overlay */}
            {
                isLoading &&
                <div className="absolute z-[1] h-screen w-screen bg-black bg-opacity-25">
                    <div className="-mt-2"><ProgressBar progress={-1} /></div>
                </div>
            }

        </div>
    );
}
