import { RoleItemListRepository } from '@/repositories/role/interface'
import { RoleDTO } from './roleData'

export class RoleApplicationService {
  constructor(
    private readonly repository: RoleItemListRepository
  ) {}

  public async list(): Promise<RoleDTO[]> {
    const items = await this.repository.list()
    return items.map(item => new RoleDTO(item))
  }
}
