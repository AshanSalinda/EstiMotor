import api from './baseApi.js'

export const adminLogin = async (credentials) => {
    const res = await api.post("/admin/login", credentials);
    return res.data;
};

export const getAllAdmins = async () => {
    const res = await api.get("/admin");
    return res.data;
};

export const createAdmin = async (admin) => {
    const res = await api.post("/admin", admin);
    return res.data;
};

export const updateEmail = async (newEmail) => {
    const res = await api.put("/admin/email", { email: newEmail });
    return res.data;
};

export const updatePassword = async (currentPassword, newPassword) => {
    const res = await api.put("/admin/password", { currentPassword, newPassword });
    return res.data;
};

export const updateAdminLevel = async (id, isSuperAdmin) => {
    const res = await api.put("/admin/level", { id, isSuperAdmin });
    return res.data;
};

export const deleteAdmin = async (id) => {
    const res = await api.delete(`/admin/${id}`);
    return res.data;
};
