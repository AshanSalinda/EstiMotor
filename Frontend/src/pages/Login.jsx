import React from 'react';
import Logo from '../../public/estimotor.png'

function Login() {
  return (
    <div className='min-w-[100vw] min-h-[100vh] bg-gray-900 flex items-center justify-center'>
        <div className='px-16 py-10 bg-black rounded-md shadow-[0_0_20px_2px_white]'>
            <h1 className='text-4xl font-medium text-center text-white'>Login</h1>
            <form className='flex flex-col items-center mt-10'>
                <input className='h-10 px-3 mt-4 text-white border border-black rounded-md outline-none bg-dark-400 w-80 focus-visible:border-primary-500' type='email' placeholder='Email'/>
                <input className='h-10 px-3 mt-4 text-white rounded-md bg-dark-400 w-80' type='password' placeholder='Password'/>
                <button className='h-10 mt-4 text-white bg-blue-500 rounded-md w-80'>Login</button>
            </form>
            <p className='mt-4 text-center cursor-pointer text-primary-500 hover:underline'>Forgot Password?</p>

            <img src={Logo} alt="logo" />
        </div>
    </div>
  )
}

export default Login