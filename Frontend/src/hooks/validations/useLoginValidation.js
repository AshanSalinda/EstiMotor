import { useForm } from "react-hook-form";


const useLoginValidation = () => {
    const { register, handleSubmit, reset, formState: { errors } } = useForm();

    const attributes = {
        email: {
            name: "email",
            label: "Email",
            helperText: errors?.['email']?.message,
            error: !!errors?.email,
            ...register('email', { 
                required: 'Email is Required.',
                pattern: {
                    value: /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/, 
                    message: "Invalid email format."
                }
            })
        },

        password: {
            name: "password",
            label: "Password",
            helperText: errors?.['password']?.message,
            error: !!errors?.password,
            ...register('password', { 
                required: 'Password is Required.',
                minLength: {
                    value: 8,
                    message: 'Must be at least 8 characters long.'
                },
                pattern: {
                    value: /^[A-Za-z0-9@.#]+$/, 
                    message: "Only A-Z, a-z, 0-9, @, ., and # are allowed."
                }
            })
        }
    }

    return { attributes, handleSubmit, reset };
};

export default useLoginValidation;