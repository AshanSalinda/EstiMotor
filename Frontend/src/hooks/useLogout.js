import { useNavigate } from "react-router-dom";

export default function useLogout() {
    const navigate = useNavigate();

    return () => {
        try {
            // Clear all cookies
            document.cookie.split(";").forEach(cookie => {
                const [name] = cookie.split("=");
                document.cookie = `${name.trim()}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
            });

            // Navigate to login
            navigate("/login");
        } catch (err) {
            console.error("Error during logout:", err);
        }
    };
}
