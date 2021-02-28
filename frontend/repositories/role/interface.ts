import { RoleItem } from '@/models/role'

export interface RoleItemResponse {
  id: number,
  name: string
}

export interface RoleItemListRepository {
  list(): Promise<RoleItem[]>
}
