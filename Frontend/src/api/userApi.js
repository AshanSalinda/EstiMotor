import selectItems from '../data/selectItems.json';
import api from './baseApi.js'


export const getPrediction = async (payload) => {
    const res = await api.post("/predict", payload);
    return res.data;
};


export function getMakeList() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(Object.keys(selectItems.models).map((make) => (
                { value: make, label: make }
            )));
    	}, 3000);
    });
}


export function getModelList(make) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(selectItems.models[make].map((model) => (
                { value: model, label: model }
            )));
    	}, 3000);
    });
}