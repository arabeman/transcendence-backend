import { UserCreateBody, userCreateSchema } from "@schemas/index";

import { FastifyInstance } from "fastify";
import { UserService } from "@services/user.service";

export default async function userRoutes(fastify: FastifyInstance) {
  const service = new UserService();

  fastify.get("/users", async () => {
    return service.findAll();
  });

  fastify.post<{
    Body: UserCreateBody;
  }>("/users", { schema: userCreateSchema }, async (req, reply) => {
    const user = await service.create(req.body);
    reply.code(201).send(user);
  });
}
