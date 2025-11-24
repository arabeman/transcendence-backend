import "reflect-metadata";

import { AppDataSource } from "./data-source";
import Fastify from "fastify";
import { config } from "dotenv";
import { envOptions } from "@config/env.schema";
import fastifyEnv from "@fastify/env";
import userRoutes from "./routes/user.route";

config();
const isProd = process.env.NODE_ENV === "production";

const fastify = Fastify({
  logger: isProd
    ? true
    : {
        transport: {
          target: "pino-pretty",
          options: {
            colorize: true,
            translateTime: "HH:MM:ss",
            ignore: "pid,hostname",
          },
        },
      },
});

const start = async () => {
  try {
    await AppDataSource.initialize();
    console.log("Data Source has been initialized!");

    // env
    await fastify.register(fastifyEnv, envOptions);

    await fastify.register(userRoutes);

    await fastify.listen({ port: fastify.config.PORT });
    console.log("Serveur démarré sur le port", fastify.config.PORT);
  } catch (err) {
    console.error("Erreur au démarrage :", err);
    process.exit(1);
  }
};

start();
