import { FromSchema } from "json-schema-to-ts";

export const userCreateSchema = {
  body: {
    type: "object",
    required: ["username", "password"],
    properties: {
      username: { type: "string", minLength: 3 },
      password: { type: "string", minLength: 6 },
    },
  },
} as const;

export type UserCreateBody = FromSchema<typeof userCreateSchema.body>;
