import { useState } from "react";
import AdminCard from "../../components/AdminCard";
import Button from '../../components/input/Button';
import useAdminInfo from "../../hooks/useAdminInfo.js";
import AddNewAdminModal from "../modals/AddNewAdminModal.jsx";
import DeleteAdminModal from "../modals/DeleteAdminModal.jsx";
import UpdateAdminLevelModal from "../modals/UpdateAdminLevelModal.jsx";

export default function TeamManagement(props) {
    const { adminList, setAdminList, showAlert, setIsLoading } = props;
    const [ openAddAdminModal, setOpenAddAdminModal ] = useState(false);
    const [ adminToLevelUpdate, setAdminToLevelUpdate ] = useState(null);
    const [ adminToDelete, setAdminToDelete ] = useState(null);
    const adminInfo = useAdminInfo() || {};

    // Ensure current admin appears first
    const sortedAdminList = [...adminList].sort((a, b) => {
        if (a.email === adminInfo.email) return -1;
        if (b.email === adminInfo.email) return 1;
        return 0;
    });

    return (
        <div className="flex flex-col items-center flex-1 space-y-16 p-4 pb-20 lg:pb-4 lg:h-full lg:overflow-y-auto">
            <h2 className="text-2xl font-medium">Team Management</h2>

            {adminInfo?.isSuperAdmin &&
                <Button
                    onClick={() => setOpenAddAdminModal(true)}
                    label="Add New Admin"
                    size="medium"
                    type="submit"
                    sx={{ width: "14rem", borderRadius: "2rem" }}
                />
            }

            <div className="space-y-4 w-[90vw] md:w-96">
                { (sortedAdminList || []).map((admin) =>
                    <AdminCard
                        key={admin.id}
                        admin={admin}
                        currentAdmin={adminInfo}
                        setAdminToLevelUpdate={setAdminToLevelUpdate}
                        setAdminToDelete={setAdminToDelete}
                    />
                ) }
                {
                    sortedAdminList.length <= 1 &&
                    <p
                        className="text-lg font-medium text-center select-none text-neutral-600" >
                        No other admins
                    </p>
                }
            </div>

            <AddNewAdminModal
                openAddAdminModal={openAddAdminModal}
                setOpenAddAdminModal={setOpenAddAdminModal}
                setAdmins={setAdminList}
                showAlert={showAlert}
                setIsLoading={setIsLoading}
            />

            <UpdateAdminLevelModal
                adminToLevelUpdate={adminToLevelUpdate}
                setAdminToLevelUpdate={setAdminToLevelUpdate}
                setAdmins={setAdminList}
                showAlert={showAlert}
                setIsLoading={setIsLoading}
            />

            <DeleteAdminModal
                adminToDelete={adminToDelete}
                setAdminToDelete={setAdminToDelete}
                setAdmins={setAdminList}
                showAlert={showAlert}
                setIsLoading={setIsLoading}
            />

        </div>
    )
}
