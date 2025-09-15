import { useEffect, useState } from "react";
import { updateAdminLevel } from "../../api/adminApi.js";
import Modal from "../../components/Modal.jsx";
import Button from '../../components/input/Button.jsx';

export default function UpdateAdminLevelModal(props) {
    const { adminToLevelUpdate, setAdminToLevelUpdate, setAdmins, showAlert, setIsLoading } = props;
    const [ isSuperAdmin, setIsSuperAdmin ] = useState(false);

    const handleClose = () => {
        setIsSuperAdmin(false)
        setAdminToLevelUpdate(null);
    }

    const handleSubmit = () => {
        setIsLoading(true);
        updateAdminLevel(adminToLevelUpdate?.id, isSuperAdmin)
            .then((data) => {
                setAdmins(data?.admins);
                showAlert(data?.message);
            })
            .catch(error => showAlert(error, "apiError"))
            .finally(() => {
                setIsLoading(false);
                handleClose();
            });
    };

    useEffect(() => {
        setIsSuperAdmin(adminToLevelUpdate?.isSuperAdmin ?? false);
    }, [adminToLevelUpdate]);

    return (
        <Modal open={adminToLevelUpdate !== null} onClose={handleClose}>
            <div className="p-6 w-[22rem] flex flex-col space-y-4">
                {/* Title */}
                <h2 className="text-xl font-semibold text-center">Update Admin Control</h2>

                {/* Description */}
                <p className="text-sm text-neutral-400 text-center">
                    Add or remove full management access <br/> for:
                </p>
                <a
                    href={`mailto:${adminToLevelUpdate?.email}`}
                    className="text-primary-400 font-medium italic break-words text-center hover:underline"
                >
                    {adminToLevelUpdate?.email}
                </a>

                {/* Toggle */}
                <label className="flex items-center justify-between p-3 bg-[#434343] rounded-md cursor-pointer">
                    <div className="space-y-0.5">
                        <span className="text-sm font-medium">Allow manage other admins</span>
                        <p className="text-xs text-neutral-400">
                            Enable this option if this admin should have the ability to create, update, or delete other admin accounts.
                        </p>
                    </div>
                    <input
                        type="checkbox"
                        checked={isSuperAdmin}
                        onChange={(e) => setIsSuperAdmin(e.target.checked)}
                        className="w-9 h-9 accent-primary-450"
                    />
                </label>

                {/* Buttons */}
                <div className="flex space-x-4 pt-6">
                    <Button label="Update" sx={{ width: "100%" }} onClick={handleSubmit} disabled={ isSuperAdmin === adminToLevelUpdate?.isSuperAdmin } />
                    <Button label="Close" sx={{ width: "100%" }} onClick={handleClose} outlined />
                </div>
            </div>
        </Modal>
    );
}
