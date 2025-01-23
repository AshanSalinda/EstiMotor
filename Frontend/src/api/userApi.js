import selectItems from '../data/selectItems.json';

export function getPrediction() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(Math.random() * 10000000);
        }, 3000);
    });
}


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