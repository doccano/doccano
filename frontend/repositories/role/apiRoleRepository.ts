import ApiService from '@/services/api.service'
import { RoleRepository } from '@/domain/models/role/roleRepository'
import { RoleItem } from '@/domain/models/role/role'

function toModel(item: { [key: string]: any }): RoleItem {
  return new RoleItem(item.id, item.name)
}

export class APIRoleRepository implements RoleRepository {
  constructor(private readonly request = ApiService) {}

  async list(): Promise<RoleItem[]> {
    const url = `/roles`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }
}
