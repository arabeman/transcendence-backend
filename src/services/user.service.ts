// src/services/user.service.ts
import { AppDataSource } from "src/data-source";
import { User } from "@entities/user.entity";
import { UserCreateBody } from "@schemas/index";

export class UserService {
  private repo = AppDataSource.getRepository(User);

  async create(data: UserCreateBody) {
    const user = this.repo.create(data);
    return this.repo.save(user);
  }

  async findAll() {
    return this.repo.find();
  }
}
