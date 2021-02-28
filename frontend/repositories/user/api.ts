import ApiService from '@/services/api.service'
import { UserItem } from '@/models/user'
import { UserItemListRepository, UserItemResponse } from './interface'

export class FromApiUserItemListRepository implements UserItemListRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(query: string): Promise<UserItem[]> {
    const url = `/users?q=${query}`
    const response = await this.request.get(url)
    const responseItems: UserItemResponse[] = response.data
    return responseItems.map(item => UserItem.valueOf(item))
  }
}
