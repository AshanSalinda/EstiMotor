import React from 'react';
import PropTypes from 'prop-types';
import { BsKey } from "react-icons/bs";
import { MdDeleteOutline } from "react-icons/md";


export default function AdminCard({ email, role }) {
  return (
    <div className='flex items-center p-4 space-x-4 rounded-md bg-dark-400 hover:bg-dark-300'>
        <span className='flex-1 overflow-hidden'>{email}</span>
        <BsKey className='text-3xl cursor-pointer text-primary-500' />
        <MdDeleteOutline className='text-3xl text-red-600 cursor-pointer' />
    </div>
  )
}


AdminCard.propTypes = {
    email: PropTypes.string,
    role: PropTypes.string
}