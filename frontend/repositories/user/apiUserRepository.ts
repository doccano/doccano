import { Page } from '@/domain/models/page'
import { UserItem } from '@/domain/models/user/user'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): UserItem {
  return new UserItem(item.id, item.username, item.is_superuser, item.is_staff)
}

function toPayload(item: { [key: string]: any }): { [key: string]: any } {
  return {
    username: item.username,
    email: item.email,
    password1: item.password1,
    password2: item.password2
  }
}

export class APIUserRepository {
  constructor(private readonly request = ApiService) {}

  async getProfile(): Promise<UserItem> {
    const url = '/me'
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async list(query: string): Promise<Page<UserItem>> {
    const url = `/users?q=${query}`
    const response = await this.request.get(url)
    return new Page(
      response.data.count,
      response.data.next,
      response.data.previous,
      response.data.results.map((item: { [key: string]: any }) => toModel(item))
    )
  }

  async create(fields: { [key: string]: any }): Promise<UserItem> {
    const url = '/users/create'
    const payload = toPayload(fields)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }
}
