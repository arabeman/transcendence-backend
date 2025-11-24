import { DataSource } from "typeorm";
import { config } from 'dotenv';

// get env
config();

export const AppDataSource = new DataSource({
    type: "sqlite",
    // database: process.env.DB_URL || "data/data.sqlite",
    database: process.env.DB_URL!,
    synchronize: process.env.NODE_ENV !== 'production',
    entities: ["src/entities/*.ts"],
    migrations: ["src/migrations/*.ts"],
    subscribers: ["src/subscribers/*.ts"],
});

