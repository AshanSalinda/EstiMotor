import mongoose from "mongoose";


const makeModelMappingSchema = new mongoose.Schema(
    {},
    { collection: "make_model_mapping", strict: false }
);

export const MakeModelMapping = mongoose.model(
    "make_model_mapping",
    makeModelMappingSchema
);
