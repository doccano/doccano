import ApiService from '@/services/api.service'
import { User, UserDetails } from '@/domain/models/user/user'

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

function toModel(item: { [key: string]: any }): User {
  return new User(
    item.id,
    item.username,
    item.email,
    item.is_active,
    item.is_superuser,
    item.is_staff
  )
}

function toModelDetails(item: { [key: string]: any }): UserDetails {
  return new UserDetails(

    item.id,
    item.username,
    item.email,
    item.first_name,
    item.last_name,
    item.is_active,
    item.is_superuser,
    item.is_staff,
    item.date_joined
  )
}

function toModelList(response: PaginatedResponse<any>): PaginatedResponse<User> {
  return {
    count: response.count,
    next: response.next,
    previous: response.previous,
    results: response.results.map((item: any) => toModel(item))
  }
}

export class APIUserRepository {
  constructor(private readonly request = ApiService) { }

  async getProfile(): Promise<User> {
    const url = '/me'
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async list(query: string): Promise<PaginatedResponse<User>> {
    const url = `/users?${query}`
    const response = await this.request.get(url)
    return toModelList(response.data);
  }

  async getUser(id: number): Promise<UserDetails> {
    const url = `/users/${id}`
    const response = await this.request.get(url)
    return toModelDetails(response.data)
  }

  async updateUser(id: number, data: { [key: string]: any }): Promise<User> {
    const url = `/users/${id}`
    const response = await this.request.patch(url, data)
    return toModel(response.data)
  }

  async deleteUser(id: number): Promise<void> {
    const url = `/users/${id}`
    await this.request.delete(url)
  }
}
