import { RoleItem } from '@/domain/models/role/role'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): RoleItem {
  return new RoleItem(item.id, item.name)
}

export class APIRoleRepository {
  constructor(private readonly request = ApiService) {}

  async list(): Promise<RoleItem[]> {
    const url = `/roles`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }
}
