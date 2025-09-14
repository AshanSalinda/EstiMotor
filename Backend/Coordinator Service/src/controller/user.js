import { MakeModelMapping } from "../models/MakeModelMapping.js";


export async function getMakeModelMapping (req, res) {
    try {
        const mappings = await MakeModelMapping.find().select("-_id") || [];
        res.status(200).json(mappings);

    } catch (err) {
        const message = "Error while fetching make-model mapping";
        console.log(message, ":", err.message);
        res.status(500).json({ message });
    }
}
