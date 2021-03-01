import { RoleItem } from '@/models/role'
import { RoleItemListRepository } from '@/repositories/role/interface'

export class RoleDTO {
  id: number
  rolename: string

  constructor(item: RoleItem) {
    this.id = item.id
    this.rolename = item.name
  }
}

export class RoleApplicationService {
  constructor(
    private readonly repository: RoleItemListRepository
  ) {}

  public async list(): Promise<RoleDTO[]> {
    const items = await this.repository.list()
    return items.map(item => new RoleDTO(item))
  }
}
