import { RoleItem } from '~/domain/models/role/role'

export interface RoleItemResponse {
  id: number,
  name: string
}

export interface RoleRepository {
  list(): Promise<RoleItem[]>
}
