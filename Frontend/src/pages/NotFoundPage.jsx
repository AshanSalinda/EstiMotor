import { useNavigate } from "react-router-dom";
import Button from "../Components/input/Button"

export default function NotFoundPage() {
    const navigate = useNavigate();

    return (
        <div className="h-screen w-screen bg-black flex items-center justify-center">
            <div className="text-center space-y-6 px-6">
                <h1 className="text-6xl font-bold">404</h1>
                <p className="text-xl">Oops! The page you’re looking for doesn’t exist.</p>
                <Button label="Back to home" outlined onClick={() => navigate("/")} />
            </div>
        </div>
    );
}
