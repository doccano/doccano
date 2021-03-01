import { UserItem } from '@/models/user'
import { UserItemListRepository } from '@/repositories/user/interface'

export class UserDTO {
  id: number
  username: string

  constructor(item: UserItem) {
    this.id = item.id
    this.username = item.username
  }
}

export class UserApplicationService {
  constructor(
    private readonly repository: UserItemListRepository
  ) {}

  public async list(query: string): Promise<UserDTO[]> {
    const items = await this.repository.list(query)
    return items.map(item => new UserDTO(item))
  }
}
