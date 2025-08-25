import { useForm } from "react-hook-form";

const useUpdateCurrentAdminValidation = (defaultEmail) => {
    const {
        register: emailRegister,
        handleSubmit: handleEmailSubmit,
        formState: { errors: emailErrors },
        watch: watchEmail,
        setValue
    } = useForm({
        defaultValues: {
            email: defaultEmail
        }
    });

    const {
        register: passwordRegister,
        handleSubmit: handlePasswordSubmit,
        formState: { errors },
        watch: watchPassword,
    } = useForm({});

    const emailValue = watchEmail("email");

    const attributes = {
        email: {
            name: "email",
            label: "Email",
            type: "text",
            inputMode: "email",
            helperText: emailErrors?.['email']?.message,
            error: !!emailErrors?.email,
            value: emailValue,
            ...emailRegister("email", {
                required: 'Email is Required.',
                pattern: {
                    value: /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/,
                    message: "Invalid email format."
                },
                onBlur: (e) => {
                    if (!e.target.value.trim()) {
                        setValue("email", defaultEmail, { shouldValidate: true }); // reset back
                    }
                }
            })
        },

        currentPassword: {
            name: "currentPassword",
            label: "Current Password",
            autoComplete: "current-password",
            helperText: errors?.['currentPassword']?.message,
            error: !!errors?.currentPassword,
            ...passwordRegister('currentPassword', {
                required: 'Current password is required.',
            })
        },

        newPassword: {
            name: "newPassword",
            label: "New Password",
            autoComplete: "new-password",
            helperText: errors?.['newPassword']?.message,
            error: !!errors?.newPassword,
            ...passwordRegister('newPassword', {
                required: 'New password is required.',
                minLength: {
                    value: 8,
                    message: 'Must be at least 8 characters long.'
                },
                pattern: {
                    value: /^[A-Za-z0-9@.#]+$/,
                    message: "Only A-Z, a-z, 0-9, @, ., and # are allowed."
                },
                validate: (val) => {
                    if (val.trim() === watchPassword("currentPassword").trim()) {
                        return "New password has no change"
                    }
                }
            })
        },

        confirmPassword: {
            name: "confirmPassword",
            label: "Confirm Password",
            autoComplete: "new-password",
            helperText: errors?.['confirmPassword']?.message,
            error: !!errors?.confirmPassword,
            ...passwordRegister('confirmPassword', {
                required: 'Please confirm your password.',
                validate: (val) => {
                    if (val !== watchPassword('newPassword')) {
                        return "Passwords do not match.";
                    }
                }
            })
        },
    };

    return { attributes, handleEmailSubmit, handlePasswordSubmit };
};

export default useUpdateCurrentAdminValidation;
