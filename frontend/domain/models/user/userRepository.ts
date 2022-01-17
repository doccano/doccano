import { UserItem } from '~/domain/models/user/user'

export interface UserRepository {
  getMe(): Promise<UserItem>

  list(query: string): Promise<UserItem[]>
}
