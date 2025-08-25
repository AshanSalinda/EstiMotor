import express from "express";
import { authMiddleware } from "../middleware/auth.js";
import {
    createAdmin,
    login,
    getAllAdmins,
    updateEmail,
    updatePassword,
    updateAdminLevel,
    deleteAdmin
} from "../controller/admin.js";

const router = express.Router();

// -----------------------
// Public route
// -----------------------
router.post("/login", login);

// -----------------------
// admin-only routes
// -----------------------
router.get("/", authMiddleware, getAllAdmins);              // List all admins
router.put("/email", authMiddleware, updateEmail);          // Update own email
router.put("/password", authMiddleware, updatePassword);    // Update own password

// -----------------------
// Superadmin-only routes
// -----------------------
router.post("/", authMiddleware, createAdmin);               // Create new admin
router.put("/level", authMiddleware, updateAdminLevel);      // Update isSuperAdmin
router.delete("/:id", authMiddleware, deleteAdmin);          // Delete admin

export default router;
