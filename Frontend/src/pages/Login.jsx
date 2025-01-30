import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';
import background from '../assets/background.jpg';
import Input from '../components/input';
import Button from '../components/input/Button';
import useLoginValidation from '../hooks/validations/useLoginValidation';
import { PiEye, PiEyeClosed } from "react-icons/pi";


function Login() {
    const [ isPasswordVisible, setIsPasswordVisible ] = useState(false);
    const { attributes, handleSubmit, reset } = useLoginValidation();

    const navigate = useNavigate();

    const onSubmit = (formData) => {
        console.log(formData);
        navigate('/model-training');
    }

    const showPasswordIcon = <button type='button' className='w-8 h-10 -mr-3 text-xl' onClick={() => setIsPasswordVisible((prev) => !prev) }>
        { isPasswordVisible ? <PiEye/> : <PiEyeClosed/>} 
    </button>

    return (
        <div className='min-w-[100vw] min-h-[100vh] overflow-auto flex items-center justify-center'>
            <img src={background} alt="background" className='absolute object-cover pointer-events-none w-full h-full brightness-[0.8]' />

            <div className='md:px-[4.5rem] w-full mx-2 md:w-fit py-11 bg-[#000000A0] backdrop-blur-sm rounded-xl shadow-[0_4px_30px_15px_#FFFFFF50] '>
                <h1 className='text-4xl font-semibold text-center text-white'>Login</h1>
                <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col items-center w-[72vw] mx-auto mt-14 space-y-2 md:w-72'>
                    <Input {...attributes.email} type='text' />
                    <Input {...attributes.password} type={isPasswordVisible ? 'text' : 'password'} ending={showPasswordIcon} />
                    <Button label='Login' type='submit' sx={{ width: "100%", }} />
                </form>
                <p className='mt-8 text-center cursor-pointer text-primary-500 hover:underline'>Forgot Password?</p>

                <img className='w-24 mx-auto mt-14' src={logo} alt="logo" />
            </div>
        </div>
    )
}

export default Login