export default function useAdminInfo() {
    try {
        const cookieStr = document.cookie
            .split("; ")
            .find(row => row.startsWith("adminInfo="))
            ?.split("=")[1];

        if (!cookieStr) return null;
        return JSON.parse(decodeURIComponent(cookieStr));
    } catch (err) {
        console.error("Failed to parse adminInfo cookie", err);
        return null;
    }
}
