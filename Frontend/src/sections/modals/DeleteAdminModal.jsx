import { deleteAdmin } from "../../api/adminApi.js";
import Button from '../../components/input/Button.jsx';
import Modal from "../../components/Modal.jsx";

export default function DeleteAdminModal(props) {
    const { adminToDelete, setAdminToDelete, setAdmins, showAlert, setIsLoading } = props;
    const { id, email } = adminToDelete || {};

    const handleClose = () => {
        setAdminToDelete(null);
    }

    const handleDelete = () => {
        setIsLoading(true);
        deleteAdmin(id)
            .then((data) => {
                setAdmins(data?.admins);
                showAlert(data?.message);
            })
            .catch(error => showAlert(error, "apiError"))
            .finally(() => {
                setIsLoading(false);
                handleClose();
            });
    }


    return (
        <Modal open={adminToDelete !== null} onClose={handleClose}>
            <div className="p-6 w-[22rem]">
                {/* Title */}
                <h2 className="text-xl font-semibold mb-6 text-center">Delete Admin</h2>

                {/* Confirmation message */}
                <p className="text-sm text-neutral-300 text-center mb-10">
                    Are you sure you want to remove <a href={`mailto:${email}`} className="text-primary-400 font-medium italic break-words hover:underline">{email}</a> from admins?
                    This action cannot be undone.
                </p>

                {/* Buttons */}
                <div className="flex justify-between space-x-4">
                    <Button
                        label="Delete"
                        onClick={handleDelete}
                        sx={{ width: "100%" }}
                        color="secondary"
                    />
                    <Button
                        label="Cancel"
                        onClick={handleClose}
                        sx={{ width: "100%" }}
                        outlined
                    />
                </div>
            </div>
        </Modal>
    )
}
