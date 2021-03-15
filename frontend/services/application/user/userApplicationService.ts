import { UserItemListRepository } from '@/repositories/user/interface'
import { UserDTO } from './userData'

export class UserApplicationService {
  constructor(
    private readonly repository: UserItemListRepository
  ) {}

  public async getMyProfile(): Promise<UserDTO> {
    const item = await this.repository.getMe()
    return new UserDTO(item)
  }

  public async list(query: string): Promise<UserDTO[]> {
    const items = await this.repository.list(query)
    return items.map(item => new UserDTO(item))
  }
}
