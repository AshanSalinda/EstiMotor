import AdminLayout from "../sections/AdminLayout";
import YourDetails from "../sections/AdminDetailsSections/YourDetails";
import OtherAdmins from "../sections/AdminDetailsSections/OtherAdmins";

export default function AdminDetails() {
    const admins = [
        {
            email: "admin1@example.com",
            role: "Super-Admin"
        },
        {
            email: "admin2@example.com",
            role: "Admin"
        },
        {
            email: "admin3@example.com",
            role: "Admin"
        },
    ]

    return (
        <AdminLayout title="Admin Details" >
            <div className="flex flex-col h-full py-5 mx-8 lg:flex-row">
                <YourDetails />

                {/* separator */}
                <div className="border-b-2 my-10 lg:my-4 lg:border-b-0 lg:border-l-[3px] border-dark-300" />
                
                <OtherAdmins admins={admins} />
                
            </div>
        </AdminLayout>
    )
}
