import { UserItem } from '@/models/user'

export interface UserItemResponse {
  id: number,
  username: string,
  is_superuser: boolean
}

export interface UserItemListRepository {
  list(query: string): Promise<UserItem[]>
}
