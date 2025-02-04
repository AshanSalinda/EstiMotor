import PropTypes from 'prop-types';
import AdminCard from "../../components/AdminCard";
import Button from '../../components/input/Button';

export default function OtherAdmins({ admins }) {
    return (
        <div className="flex flex-col items-center flex-1 h-full p-4 space-y-16 lg:overflow-y-auto">
            <h2 className="text-2xl font-semibold">Other Admins</h2>

            <Button 
                label="Add New Admin" 
                size="medium"
                type="submit"
                sx={{ width: "14rem", borderRadius: "2rem" }}
            />

            <div className="space-y-4 w-[90vw] md:w-96">
                { admins.length > 0 ?
                    admins.map(({ email, role }) => <AdminCard key={email} email={email} role={role} />) :
                    <p className="text-lg font-medium text-center select-none text-neutral-600">No other admins</p> 
                }
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
