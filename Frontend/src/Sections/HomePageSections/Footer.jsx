import React from 'react';
import logo from '../../assets/logo.svg';


function Footer() {
    return (
        <footer className="py-16 text-white bg-gray-900 bg-opacity-45">
            <div className="container px-6 mx-auto md:px-12 lg:px-20">
                {/* Grid Layout */}
                <div className="grid grid-cols-1 gap-12 md:grid-cols-3">

                    {/* Logo and Description */}
                    <div className="flex flex-col items-center md:items-start">
                        <img src={logo} alt="EstiMotor Logo" className="w-40 mb-6" />
                        <p className="max-w-sm text-sm text-center text-gray-300 md:text-left">
                            EstiMotor leverages AI-driven analytics to bring transparency and accuracy to the used vehicle market. Get reliable price insights instantly.
                        </p>
                    </div>

                    {/* Quick Links */}
                    <div className="flex justify-center">
                        <div className="flex flex-col space-y-4">
                            <h3 className="text-lg font-semibold text-gray-100">Quick Links</h3>
                            <ul className="space-y-2">
                                <li>
                                    <a href="/privacy-policy" className="text-sm text-gray-300 transition-colors hover:text-white">
                                        Privacy Policy
                                    </a>
                                </li>
                                <li>
                                    <a href="/terms-of-service" className="text-sm text-gray-300 transition-colors hover:text-white">
                                        Terms of Service
                                    </a>
                                </li>
                                <li>
                                    <a href="/about" className="text-sm text-gray-300 transition-colors hover:text-white">
                                        About Us
                                    </a>
                                </li>
                            </ul>
                        </div>

                    </div>

                    {/* Contact */}
                    <div className="flex justify-center">
                        <div className="flex flex-col items-center space-y-4">
                            <h3 className="text-lg font-semibold text-gray-100">Contact</h3>
                            <p className="text-sm text-gray-300">Have questions? Reach out to us:</p>
                            <a href="mailto:contact@estimotor.com" className="text-sm text-blue-400 transition-colors hover:text-blue-300">
                                contact@estimotor.com
                            </a>
                        </div>
                    </div>
                </div>

                {/* Divider */}
                <div className="my-8 border-t border-gray-700"></div>

                {/* Copyright */}
                <div >
                    <p className="text-xs text-center text-gray-400">
                        © 2024 EstiMotor. All rights reserved.
                    </p>
                </div>
            </div>
        </footer>
    );
}

export default Footer;