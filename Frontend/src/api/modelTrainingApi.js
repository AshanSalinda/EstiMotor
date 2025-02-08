import axios from 'axios';

export function startTraining() {
    return axios.post('http://localhost:8000/start');
}

export function stopTraining() {
    return axios.post('http://localhost:8000/stop');
}