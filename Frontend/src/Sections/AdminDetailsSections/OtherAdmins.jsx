import PropTypes from 'prop-types';
import AdminCard from "../../components/AdminCard";

export default function OtherAdmins({ admins }) {
    return (
        <div className="flex flex-col items-center flex-grow h-full p-4 space-y-16 lg:overflow-y-auto">
            <h2 className="text-2xl font-semibold">Other Admins</h2>

            <div className="space-y-4 w-[90vw] md:w-96">
                {admins.map(({ email, role }) => <AdminCard key={email} email={email} role={role} />)}
            </div>
        </div>
    )
}

OtherAdmins.propTypes = {
    admins: PropTypes.arrayOf(
        PropTypes.shape({
            email: PropTypes.string,
            role: PropTypes.string,
        })
    ),
};
