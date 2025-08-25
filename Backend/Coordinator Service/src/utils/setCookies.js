import jwt from "jsonwebtoken";

export default function setCookies(res, admin) {
    // Generate JWT Token
    const token = jwt.sign(
        { id: admin._id, email: admin.email, isSuperAdmin: admin.isSuperAdmin },
        process.env.JWT_SECRET,
        { expiresIn: "1d" }
    );

    // Secure httpOnly cookie with JWT (not accessible by JS)
    res.cookie("token", token, {
        httpOnly: true,
        secure: false,
        sameSite: "strict",
        maxAge: 24 * 60 * 60 * 1000 // 1 day in ms
    });

    // Public cookie with minimal user info (accessible by FE)
    res.cookie("adminInfo", JSON.stringify({
        email: admin.email,
        isSuperAdmin: admin.isSuperAdmin
    }), {
        httpOnly: false, // FE can read it
        secure: false,
        sameSite: "strict",
        maxAge: 24 * 60 * 60 * 1000 // 1 day in ms
    });
}
