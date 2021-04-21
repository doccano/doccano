import { UserItem } from '~/domain/models/user/user'

export interface UserItemResponse {
  id: number,
  username: string,
  is_superuser: boolean
}

export interface UserRepository {
  getMe(): Promise<UserItem>

  list(query: string): Promise<UserItem[]>
}
