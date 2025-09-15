import express from "express";
import { getMakeModelMapping } from "../controller/user.js";

const router = express.Router();

router.get("/make-model-map", getMakeModelMapping);     // Fetch make-model mapping

export default router;
