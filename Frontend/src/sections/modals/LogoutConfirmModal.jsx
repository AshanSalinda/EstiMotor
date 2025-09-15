import Modal from "../../components/Modal.jsx";
import Button from "../../components/input/Button";

export default function LogoutConfirmModal({ open, onClose, onConfirm }) {

    return (
        <Modal open={open} onClose={onClose}>
            <div className="p-6 w-[22rem]">
                {/* Title */}
                <h2 className="text-xl font-semibold mb-6 text-center">Confirm Logout</h2>

                {/* Description */}
                <p className="text-sm text-neutral-400 mb-10 text-center">
                    Are you sure you want to log out? You will need to log in again to access your account.
                </p>

                {/* Buttons */}
                <div className="flex justify-between space-x-4">
                    <Button
                        label="Logout"
                        sx={{ width: "100%" }}
                        onClick={onConfirm}
                        color="secondary"
                    />
                    <Button
                        label="Cancel"
                        sx={{ width: "100%" }}
                        onClick={onClose}
                        outlined
                    />
                </div>
            </div>
        </Modal>
    );
}
