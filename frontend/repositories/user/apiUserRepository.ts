import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { UserRepository } from '@/domain/models/user/userRepository'
import { UserItem } from '~/domain/models/user/user'

export class APIUserRepository implements UserRepository {
  constructor(private readonly request = ApiService) {}

  async getMe(): Promise<UserItem> {
    const url = '/me'
    const response = await this.request.get(url)
    return plainToInstance(UserItem, response.data)
  }

  async list(query: string): Promise<UserItem[]> {
    const url = `/users?q=${query}`
    const response = await this.request.get(url)
    return response.data.map((item: any) => plainToInstance(UserItem, item))
  }
}
