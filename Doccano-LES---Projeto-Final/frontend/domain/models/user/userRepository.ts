import { UserItem } from './user'

export interface UserRepository {
  create(item: UserItem): Promise<UserItem>
  list(): Promise<UserItem[]>
  delete(id: number): Promise<UserItem>
  update(id: number, data: Partial<UserItem>): Promise<UserItem>
}
