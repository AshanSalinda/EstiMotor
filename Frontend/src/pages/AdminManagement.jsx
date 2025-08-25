import { useEffect, useState } from "react";
import AdminLayout from "../sections/AdminLayout";
import AccountManagement from "../Sections/AdminManagementSections/AccountManagement.jsx";
import TeamManagement from "../Sections/AdminManagementSections/TeamManagement.jsx";
import { getAllAdmins } from "../api/adminApi.js";
import { useAlert } from "../context/AlertContext.jsx";

export default function AdminManagement() {
    const [ adminList, setAdminList ] = useState([]);
    const [ isLoading, setIsLoading ] = useState(false);
    const { showAlert } = useAlert();

    useEffect(() => {
        setIsLoading(true);
        getAllAdmins()
            .then(data => setAdminList(data))
            .catch(error => showAlert(error, "apiError"))
            .finally(() => setIsLoading(false));
    }, [])

    return (
        <AdminLayout title="Admin Management" isLoading={isLoading} >
            <div className="flex flex-col h-full py-5 lg:flex-row">
                <AccountManagement {...{setAdminList, showAlert, setIsLoading}} />

                {/* separator */}
                <div className="border-b-2 my-10 lg:my-4 lg:border-b-0 lg:border-l-[3px] border-dark-300" />
                
                <TeamManagement {...{adminList, setAdminList, showAlert, setIsLoading}} />
                
            </div>
        </AdminLayout>
    )
}
