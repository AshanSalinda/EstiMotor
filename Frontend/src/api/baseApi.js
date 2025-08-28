import axios from "axios";
import useLogout from "../hooks/useLogout.js";


const api = axios.create({
    baseURL: import.meta.env.VITE_BE_BASE_URL, // Coordinator service
    withCredentials: true,                     // send cookies automatically
});

// Response interceptor
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            const logout = useLogout();
            logout();
        }
        return Promise.reject(error);
    }
);

export default api;
