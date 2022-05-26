import { UserDTO } from './userData'
import { UserRepository } from '~/domain/models/user/userRepository'

export class UserApplicationService {
  constructor(private readonly repository: UserRepository) {}

  public async getMyProfile(): Promise<UserDTO> {
    const item = await this.repository.getMe()
    return new UserDTO(item)
  }

  public async list(query: string): Promise<UserDTO[]> {
    const items = await this.repository.list(query)
    return items.map((item) => new UserDTO(item))
  }
}
