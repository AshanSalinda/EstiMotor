import api from "./baseApi.js";

export const startTraining = async () => {
    const res = await api.post("/scraping/start");
    return res.data;
};

export const stopTraining = async () => {
    const res = await api.post("/scraping/stop");
    return res.data;
};
