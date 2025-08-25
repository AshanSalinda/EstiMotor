import React from 'react';
import { BsKey } from "react-icons/bs";
import { MdDeleteOutline } from "react-icons/md";

export default function AdminCard({ admin, currentAdmin, setAdminToLevelUpdate, setAdminToDelete }) {
    const { email, isSuperAdmin } = admin || {};
    const { email: selfEmail, isSuperAdmin: isSelfSuperAdmin } = currentAdmin;

    const handleDeleteClick = () => {
        if (isSelfSuperAdmin) {
            setAdminToDelete(admin);
        }
    };

    const handleLevelUpdateClick = () => {
        if (isSelfSuperAdmin) {
            setAdminToLevelUpdate(admin);
        }
    };

    return (
        <div className="flex items-center py-2 justify-between rounded-md bg-dark-400 hover:bg-dark-400">
            <span className="px-4 flex-1 overflow-hidden text-ellipsis whitespace-nowrap">{email}</span>

            {/*icons container*/}
            <div className="flex items-center pr-2 space-x-1">
                {/* If same as logged-in user → show blue circle */}
                { selfEmail === email ? (
                    <div className="w-3 h-3 m-4 rounded-full bg-primary-500" />
                ) : (
                    <>
                        {/* Show key icon always (highlight if superAdmin) */}
                        <div
                            onClick={handleLevelUpdateClick}
                            className={`p-1.5 rounded-full ${isSelfSuperAdmin ? "hover:bg-dark-200 hover:bg-opacity-30 cursor-pointer" : "pointer-events-none"}`}
                        >
                            <BsKey className={`text-3xl ${isSuperAdmin ? "text-primary-500" : "text-dark-200"}`} />
                        </div>

                        {/* Show delete only if superAdmin */}
                        {isSelfSuperAdmin && (
                            <div
                                onClick={handleDeleteClick}
                                className="p-1.5 rounded-full hover:bg-dark-200 hover:bg-opacity-30 cursor-pointer"
                            >
                                <MdDeleteOutline className="text-3xl text-red-600" />
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}
