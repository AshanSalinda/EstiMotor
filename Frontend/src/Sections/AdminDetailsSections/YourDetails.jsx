import React from 'react';
import Input from '../../components/input';
import Button from '../../components/input/Button';

export default function YourDetails() {
  return (
    <div className="flex flex-col items-center flex-grow h-full p-4 space-y-16 lg:overflow-y-auto">
        <h2 className="text-2xl font-semibold">Your Details</h2>

        <form className="flex flex-col items-center space-y-1 w-[90vw] md:w-80">
            
            <Input type="text" label="Email" />

            <Button 
                label="Update Email" 
                size="medium"
                type="submit"
                sx={{ width: "14rem", borderRadius: "2rem" }}
            />
        </form>

        <form className="flex flex-col items-center space-y-1 w-[90vw] md:w-80">

            <Input type="text" label="Current Password" />
            <Input type="text" label="New Password" />
            <Input type="text" label="Confirm Password" />
            
            <Button 
                label="Change Password" 
                size="medium"
                type="submit"
                sx={{ width: "14rem", borderRadius: "2rem" }}
            />
        </form>
    </div>
  )
}
