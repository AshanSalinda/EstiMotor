import mongoose from "mongoose";

export const connectDB = async () => {
    try {
        const mongoURI = process.env.MONGO_URI;
        const databaseName = process.env.DATABASE_NAME;

        if (!mongoURI) {
            throw new Error("'MongoDB_URI' is missing in environment variable");
        }

        if (!databaseName) {
            throw new Error("'DATABASE_NAME' is missing in environment variable");
        }

        await mongoose.connect(process.env.MONGO_URI,{
            dbName: process.env.DATABASE_NAME,
            serverApi: {
                version: '1',
                strict: true,
                deprecationErrors: true
            }
        });
        console.log("✅  MongoDB connected");
    } catch (err) {
        console.error("❌  MongoDB connection error:", err.message);
        process.exit(1);
    }
};
