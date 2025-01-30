import { Routes, Route } from 'react-router-dom';
import ModelTraining from '../pages/ModelTraining';

export default function AdminRoutes() {
    return (
        <Routes>
            <Route path="/model-training" element={<ModelTraining />} />
            <Route path="/*" element={<div className="text-red-500">Page Not Found...</div>} />
        </Routes>
    )
}
