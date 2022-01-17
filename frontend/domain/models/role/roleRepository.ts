import { RoleItem } from '~/domain/models/role/role'

export interface RoleRepository {
  list(): Promise<RoleItem[]>
}
