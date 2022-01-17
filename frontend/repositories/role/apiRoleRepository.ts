import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { RoleRepository } from '../../domain/models/role/roleRepository'
import { RoleItem } from '~/domain/models/role/role'

export class APIRoleRepository implements RoleRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(): Promise<RoleItem[]> {
    const url = `/roles`
    const response = await this.request.get(url)
    return response.data.map((item: any) => plainToInstance(RoleItem, item))
  }
}
