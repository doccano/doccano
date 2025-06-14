import { UserDTO } from './userData'
import { CreateUserCommand } from './userCommand'
import { UserRepository } from '~/domain/models/user/userRepository'
import { UserItem } from '~/domain/models/user/user'

export class UserApplicationService {
  constructor(private readonly repository: UserRepository) {}

  public async create(item: CreateUserCommand): Promise<UserDTO> {
    const user = UserItem.create(
      item.username,
      item.password,
      item.passwordConfirmation,
      item.isSuperUser,
      item.isStaff,
      item.first_name,
      item.last_name,
      item.email
    )
    const created = await this.repository.create(user)
    return new UserDTO(created)
  }

  public async list(): Promise<UserDTO[]> {
    const users = await this.repository.list()
    return users.map((user) => new UserDTO(user))
  }

  public async delete(userId: number): Promise<void> {
    await this.repository.delete(userId)
  }

  public async update(userId: number, data: Partial<CreateUserCommand>): Promise<UserDTO> {
    const updated = await this.repository.update(userId, data)
    return new UserDTO(updated)
  }
}
