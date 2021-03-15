import ApiService from '@/services/api.service'
import { RoleItemListRepository, RoleItemResponse } from './interface'
import { RoleItem } from '~/domain/models/role/role'

export class FromApiRoleItemListRepository implements RoleItemListRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(): Promise<RoleItem[]> {
    const url = `/roles`
    const response = await this.request.get(url)
    const responseItems: RoleItemResponse[] = response.data
    return responseItems.map(item => RoleItem.valueOf(item))
  }
}
