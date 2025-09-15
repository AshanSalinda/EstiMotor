import React from 'react';
import { Modal as MuiModal } from '@mui/material';
import { MdOutlineClose } from "react-icons/md";

export default function Modal({ open, onClose, children }) {
    return (
        <MuiModal
            open={open}
            onClose={onClose}
        >
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-fit rounded-lg bg-dark-300 px-4 py-7">
                {/* Close Button */}
                <button
                    onClick={onClose}
                    className="absolute top-3 right-3 text-primary-300 hover:text-gray-200 transition-colors text-2xl"
                    aria-label="Close modal"
                >
                    <MdOutlineClose />
                </button>

                {/* Modal Content */}
                {children}
            </div>
        </MuiModal>
    );
}
