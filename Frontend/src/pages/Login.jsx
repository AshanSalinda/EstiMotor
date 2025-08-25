import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Input from '../components/input';
import Button from '../components/input/Button';
import useLoginValidation from '../hooks/validations/useLoginValidation';
import { PiEye, PiEyeClosed } from "react-icons/pi";
import { adminLogin } from "../api/adminApi.js";
import { useAlert } from "../context/AlertContext.jsx";
import ProgressBar from "../Components/ProgressBar.jsx";


function Login() {
    const [ isPasswordVisible, setIsPasswordVisible ] = useState(false);
    const [ isLoading, setIsLoading ] = useState(false);
    const { attributes, handleSubmit } = useLoginValidation();

    const navigate = useNavigate();
    const { showAlert } = useAlert();

    const onSubmit = (formData) => {
        setIsLoading(true);
        adminLogin(formData)
            .then(() => {
                navigate('/model-training');
            })
            .catch(error => showAlert(error, "apiError"))
            .finally(() => setIsLoading(false));
    }

    const showPasswordIcon = <button 
        type='button' 
        aria-label={isPasswordVisible ? "Hide password" : "Show password"} 
        className='w-8 h-10 -mr-3 text-xl' 
        onClick={() => setIsPasswordVisible((prev) => !prev) } >
        { isPasswordVisible ? <PiEye/> : <PiEyeClosed/>} 
    </button>

    return (
        <div className='min-w-[100vw] min-h-[100vh] overflow-auto flex items-center justify-center'>
            <img src="/login-background.webp" alt="background" className='absolute object-cover w-full h-full pointer-events-none contrast-[1.1] brightness-90' />

            <div className='md:px-[4.4rem] w-full mx-2 md:w-fit py-11 bg-[#000000A0] backdrop-blur-sm rounded-xl shadow-[0_4px_30px_15px_#FFFFFF50] '>
                <h1 className='text-4xl font-semibold text-center text-white'>Login</h1>
                <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col items-center w-[72vw] mx-auto mt-14 space-y-4 md:space-y-2 md:w-72'>
                    <Input {...attributes.email} />
                    <Input {...attributes.password} type={isPasswordVisible ? 'text' : 'password'} ending={showPasswordIcon} />
                    <Button label={!isLoading ? 'Login' : 'Logging In'} type='submit' sx={{ width: "100%" }} />
                </form>
                <p className='mt-8 text-center cursor-pointer text-primary-500 hover:underline'>Forgot Password?</p>

                <img className='w-24 mx-auto mt-14' src="/logo.svg" alt="logo" />
            </div>

            {/* Loading overlay */}
            {
                isLoading &&
                <div className="absolute z-[1] h-screen w-screen bg-black bg-opacity-25">
                    <div className="-mt-2"><ProgressBar progress={-1} /></div>
                </div>
            }
        </div>
    )
}

export default Login