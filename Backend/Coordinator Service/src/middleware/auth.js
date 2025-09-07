import jwt from "jsonwebtoken";

export let invalidatedAdmins = new Set();

export function authMiddleware(req, res, next) {
    const token = req.cookies?.token; // JWT stored in cookie

    if (!token) {
        return res.status(401).json({ message: "Unauthorized" });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);

        if (invalidatedAdmins.has(decoded.id)) {
            return res.status(401).json({ error: "Session expired due to role update" });
        }

        req.user = decoded; // make user info available downstream
        next();
    } catch (err) {
        return res.status(401).json({ message: "Session expired" });
    }
}
