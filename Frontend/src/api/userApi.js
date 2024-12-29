export function getPrediction() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(Math.random() * 10000000);
        }, 3000);
    });
}