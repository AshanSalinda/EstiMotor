import mongoose from "mongoose";

const adminSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    isSuperAdmin: { type: Boolean, default: false }
});

export const Admin = mongoose.model("admin_users", adminSchema);
