export const envSchema = {
    type: "object",
    required: ["DB_URL"],
    properties: {
        PORT: {
            type: "number",
            default: 3000,
        },
        DB_URL: {
            type: "string",
        },
        NODE_ENV: {
            type: "string",
            enum: ["development", "production"],
            default: "development",
        },
    },
};

export const envOptions = {
    confKey: "config",
    schema: envSchema,
    dotenv: true,
    data: process.env,
};

