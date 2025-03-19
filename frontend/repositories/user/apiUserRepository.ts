import { UserItem } from '@/domain/models/user/user'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): UserItem {
  return new UserItem(item.id, item.username, item.is_superuser, item.is_staff)
}

export class APIUserRepository {
  constructor(private readonly request = ApiService) {}

  async getProfile(): Promise<UserItem> {
    const url = '/me'
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async list(query: string): Promise<UserItem[]> {
    const url = `/users?q=${query}`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async delete(id: number): Promise<void> {
    const url = `/users/delete/${id}`
    await this.request.delete(url)
  }

  async getIdByUsername(username: string): Promise<number> {
    // Reuse the list method to fetch users matching the query.
    const users = await this.list(username);
    // Find the user with the exact username.
    const foundUser = users.find(user => user.username === username);
    if (!foundUser) {
      throw new Error(`⁠User with username ${username} not found.`);
    }
    return foundUser.id;
  }
}
