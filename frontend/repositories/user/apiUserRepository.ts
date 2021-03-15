import ApiService from '@/services/api.service'
import { UserRepository, UserItemResponse } from '@/domain/models/user/userRepository'
import { UserItem } from '~/domain/models/user/user'

export class APIUserRepository implements UserRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async getMe(): Promise<UserItem> {
    const url = '/me'
    const response = await this.request.get(url)
    const item: UserItemResponse = response.data
    return UserItem.valueOf(item)
  }

  async list(query: string): Promise<UserItem[]> {
    const url = `/users?q=${query}`
    const response = await this.request.get(url)
    const responseItems: UserItemResponse[] = response.data
    return responseItems.map(item => UserItem.valueOf(item))
  }
}
