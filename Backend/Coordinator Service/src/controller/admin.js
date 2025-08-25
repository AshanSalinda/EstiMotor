import { Admin } from "../models/Admin.js";
import { invalidatedAdmins } from "../middleware/auth.js";
import setCookies from "../utils/setCookies.js";
import { hashPassword, comparePassword } from "../utils/hash.js";


export async function login (req, res) {
    try {
        const email = req?.body?.email;
        const password = req?.body?.password;

        if (!email || !password){
            return res.status(400).json({ message: "Invalid credentials" });
        }

        const admin = await Admin.findOne({ email });
        if (!admin) return res.status(400).json({ message: "Invalid credentials" });

        const isMatch = await comparePassword(password, admin?.password);
        if (!isMatch) return res.status(400).json({ message: "Invalid credentials" });

        setCookies(res, admin)

        // remove after login if marked as invalid
        if (invalidatedAdmins.has(admin._id)) {
            invalidatedAdmins.delete(admin._id);
        }

        res.status(200).json({ message: "Successfully logged in" });

    } catch (err) {
        const message = "Error while login";
        console.log(message, ": ", err.message);
        res.status(500).json({ message });
    }
}


export async function getAllAdmins (req, res) {
    try {
        res.status(200).json(await fetchAllAdmins());

    } catch (err) {
        const message = "Error while fetching admins";
        console.log(message, ":", err.message);
        res.status(500).json({ message });
    }
}


export async function createAdmin (req, res) {
    try {
        if (!req?.user?.isSuperAdmin) {
            return res.status(403).json({ message: "Only super admins can create admins" });
        }

        const email = req?.body?.email;
        const password = req?.body?.password;
        const isSuperAdmin = req?.body?.isSuperAdmin || false

        if (!email || !password) {
            return res.status(400).json({ message: "email or password not provided for new admin" });
        }

        const existing = await Admin.findOne({ email });
        if (existing) {
            return res.status(400).json({ message: "Admin already exists" });
        }

        const hashedPassword = await hashPassword(password);
        const admin = new Admin({ email, password: hashedPassword, isSuperAdmin });
        await admin.save();

        res.status(201).json({
            message: "New Admin created successfully",
            admins: await fetchAllAdmins()
        });

    } catch (err) {
        const message = "Error while creating admin";
        console.log(message, ":", err.message);
        res.status(500).json({ message });
    }
}


export async function updateEmail(req, res) {
    try {
        const newEmail = req?.body?.email;

        if (!newEmail) return res.status(400).json({ message: "Email not provided" });

        // Check if email already exists in other accounts
        const isAlreadyInUse = await Admin.exists({ email: newEmail });
        if (isAlreadyInUse) {
            return res.status(400).json({ message: "Email already in use" });
        }

        // Admin can only update their own email
        const adminToUpdate = await Admin.findById(req.user.id);
        if (!adminToUpdate) return res.status(404).json({ message: "Admin not found to update" });

        // Update email
        adminToUpdate.email = newEmail;
        await adminToUpdate.save();

        // set cookies with updated info
        setCookies(res, adminToUpdate)

        res.status(200).json({
            message: "Email updated successfully",
            admins: await fetchAllAdmins()
        });

    } catch (err) {
        const message = "Error while updating email";
        console.log(message, ":", err.message);
        res.status(500).json({ message });
    }
}


export async function updatePassword(req, res) {
    try {
        const currentPassword = req?.body?.currentPassword;
        const newPassword = req?.body?.newPassword;

        if (!currentPassword || !newPassword) {
            return res.status(400).json({ message: "currentPassword or newPassword not provided" });
        }

        // Admin can only update their own password
        const adminToUpdate = await Admin.findById(req.user.id);
        if (!adminToUpdate) return res.status(404).json({ message: "Admin not found to update" });

        // Verify current password
        const isMatch = await comparePassword(currentPassword, adminToUpdate?.password);
        if (!isMatch) return res.status(400).json({ message: "Incorrect current password" });

        // Hash and save new password
        adminToUpdate.password = await hashPassword(newPassword);
        await adminToUpdate.save();

        res.status(200).json({ message: "Password updated successfully" });

    } catch (err) {
        const message = "Error while updating password";
        console.log(message, ":", err.message);
        res.status(500).json({ message });
    }
}


export async function updateAdminLevel(req, res) {
    try {
        const isSuperAdmin = req?.body?.isSuperAdmin;
        const targetAdminId = req?.body?.id;

        if (!targetAdminId || isSuperAdmin === null || isSuperAdmin === undefined) {
            return res.status(400).json({ message: "Incomplete payload provided" });
        }

        // Only superadmins can update others
        if (!req.user.isSuperAdmin) {
            return res.status(403).json({ message: "Only super admins can update this field" });
        }

        // Admin cannot modify their own isSuperAdmin status
        if (req.user.id === targetAdminId) {
            return res.status(403).json({ message: "Cannot modify your own admin status" });
        }

        const adminToUpdate = await Admin.findById(targetAdminId);
        if (!adminToUpdate) return res.status(404).json({ message: "Admin not found to update" });

        adminToUpdate.isSuperAdmin = Boolean(isSuperAdmin);
        await adminToUpdate.save();

        invalidatedAdmins.add(adminToUpdate._id);

        res.status(200).json({
            message: "Admin access updated successfully",
            admins: await fetchAllAdmins()
        });

    } catch (err) {
        const message = "Error while updating admin access";
        console.log(message, ":", err.message);
        res.status(500).json({ message });
    }
}


export async function deleteAdmin(req, res) {
    try {
        if (!req.user.isSuperAdmin) {
            return res.status(403).json({ message: "Only super admins can delete admins" });
        }

        const foundById = await Admin.findByIdAndDelete(req.params.id);

        if (!foundById) return res.status(404).json({ message: "Admin not found to delete" });

        invalidatedAdmins.add(req.params.id);

        res.status(200).json({
            message: "Admin deleted",
            admins: await fetchAllAdmins()
        });

    } catch (err) {
        const message = "Error while deleting admin";
        console.log(message, ":", err.message);
        res.status(500).json({ message });
    }
}


async function fetchAllAdmins() {
    const admins = await Admin.find().select("-password -__v").lean() || [];

    return admins.map(({ _id, ...rest }) => ({
        id: _id.toString(),
        ...rest,
    }));
}
