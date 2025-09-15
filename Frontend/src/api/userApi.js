import api from './baseApi.js'


export const getPrediction = async (payload) => {
    const res = await api.post("/predict", payload);
    return res.data;
};

export const getMakeModelMapping = async () => {
    const res = await api.get("/api/make-model-map");
    return res.data;
};
