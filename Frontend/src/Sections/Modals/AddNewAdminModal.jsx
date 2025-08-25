import Input from '../../Components/input/index.jsx';
import Button from '../../Components/input/Button.jsx';
import Modal from "../../Components/Modal.jsx";
import useAddNewAdminValidation from "../../hooks/validations/useAddNewAdminValidation.js";
import { createAdmin } from "../../api/adminApi.js";

export default function AddNewAdminModal(props) {
    const { openAddAdminModal, setOpenAddAdminModal, setAdmins, showAlert, setIsLoading } = props;
    const { attributes, handleSubmit, reset } = useAddNewAdminValidation();

    const handleClose = () => {
        reset();
        setOpenAddAdminModal(false);
    }

    const onSubmit = (newAdmin) => {
        setIsLoading(true);
        createAdmin(newAdmin)
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
        <Modal open={openAddAdminModal} onClose={handleClose}>
            <div className="p-6 w-[22rem]">
                {/* Title */}
                <h2 className="text-xl font-semibold mb-6 text-center">Add New Admin</h2>

                {/* Form */}
                <form className="space-y-2" onSubmit={handleSubmit(onSubmit)} >
                    {/* Email */}
                    <Input {...attributes.email} />
                    <Input {...attributes.password} />

                    {/* isSuperAdmin toggle */}
                    <label className="flex items-center justify-between p-3 bg-[#434343] rounded-md cursor-pointer">
                        <div className="space-y-0.5">
                            <span className="text-sm font-medium">Allow manage other admins</span>
                            <p className="text-xs text-neutral-400">
                                Enable this option if the new admin should have the ability to create, update, or delete other admin accounts.
                            </p>
                        </div>
                        <input {...attributes.isSuperAdmin} className="w-10 h-10 accent-primary-450" />
                    </label>

                    {/* Buttons */}
                    <div className="flex justify-between pt-6 space-x-4">
                        <Button label='Add' type='submit' sx={{ width: "100%" }} />
                        <Button label="Close" sx={{ width: "100%" }} outlined onClick={handleClose} />
                    </div>
                </form>
            </div>
        </Modal>
    )
}
