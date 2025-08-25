import { useState } from "react";
import Input from '../../components/input';
import Button from '../../components/input/Button';
import useAdminInfo from "../../hooks/useAdminInfo.js";
import useLogout from "../../hooks/useLogout.js";
import useUpdateCurrentAdminValidation from "../../hooks/validations/useUpdateCurrentAdminValidation.js";
import { updateEmail, updatePassword } from "../../api/adminApi.js";
import { PiEye, PiEyeClosed } from "react-icons/pi";
import LogoutConfirmModal from "../Modals/LogoutConfirmModal.jsx";


export default function AccountManagement(props) {
    const { setAdminList, showAlert, setIsLoading } = props;

    const [ isCurrentPasswordVisible, setCurrentPasswordVisible ] = useState(false);
    const [ isNewPasswordVisible, setNewPasswordVisible ] = useState(false);
    const [ isConfirmPasswordVisible, setConfirmPasswordVisible ] = useState(false);
    const [ openLogoutConfirmModal, setOpenLogoutConfirmModal ] = useState(false);

    const logout = useLogout();
    const adminInfo = useAdminInfo();
    const { attributes, handleEmailSubmit, handlePasswordSubmit } = useUpdateCurrentAdminValidation(adminInfo?.email);

    const onEmailSubmit = (formData) => {
        if (formData.email.trim() === adminInfo?.email) {
            showAlert("Email must be different from current", "error");
            return;
        }

        setIsLoading(true);
        updateEmail(formData?.email.trim())
            .then((data) => {
                setAdminList(data?.admins);
                showAlert(data?.message);
            })
            .catch(error => showAlert(error, "apiError"))
            .finally(() => setIsLoading(false));
    };

    const onPasswordSubmit = (formData) => {
        setIsLoading(true);
        updatePassword(formData?.currentPassword, formData?.confirmPassword)
            .then(() => logout())
            .catch(error => showAlert(error, "apiError"))
            .finally(() => setIsLoading(false));
    };

    const getEndingIcon = (isPasswordVisible, setPasswordVisible) => {
        return (
            <button
                type='button'
                aria-label={isPasswordVisible ? "Hide password" : "Show password"}
                className='w-8 h-10 -mr-3 text-xl'
                onClick={() => setPasswordVisible((prev) => !prev) } >
                { isPasswordVisible ? <PiEye/> : <PiEyeClosed/>}
            </button>
        )
    }


    return (
        <div className="flex flex-col items-center flex-1 p-4 space-y-16 lg:h-full lg:overflow-y-auto scrollable">
            <h2 className="text-2xl font-medium">Account Management</h2>

            <form onSubmit={handleEmailSubmit(onEmailSubmit)} className="flex flex-col items-center space-y-1 w-[90vw] md:w-80">

                <Input {...attributes.email} />

                <Button
                    label="Update Email"
                    size="medium"
                    type="submit"
                    sx={{ width: "14rem", borderRadius: "2rem" }}
                />
            </form>

            <form onSubmit={handlePasswordSubmit(onPasswordSubmit)} className="flex flex-col items-center space-y-2 w-[90vw] md:w-80">

                <Input
                    {...attributes.currentPassword}
                    type={isCurrentPasswordVisible ? 'text' : 'password'}
                    ending={getEndingIcon(isCurrentPasswordVisible, setCurrentPasswordVisible)}
                />

                <Input
                    {...attributes.newPassword}
                    type={isNewPasswordVisible ? 'text' : 'password'}
                    ending={getEndingIcon(isNewPasswordVisible, setNewPasswordVisible)}
                />

                <Input
                    {...attributes.confirmPassword}
                    type={isConfirmPasswordVisible ? 'text' : 'password'}
                    ending={getEndingIcon(isConfirmPasswordVisible, setConfirmPasswordVisible)}
                />

                <Button
                    label="Change Password"
                    size="medium"
                    type="submit"
                    sx={{ width: "14rem", borderRadius: "2rem" }}
                />
            </form>

            <div className="flex justify-center w-[90vw] md:w-80">
                <Button
                    label="Logout"
                    size="medium"
                    color="secondary"
                    sx={{ width: "14rem", borderRadius: "2rem" }}
                    onClick={() => setOpenLogoutConfirmModal(true)}
                />
            </div>

            <LogoutConfirmModal
                open={openLogoutConfirmModal}
                onClose={() => setOpenLogoutConfirmModal(false)}
                onConfirm={logout}
            />
        </div>
    )
}
