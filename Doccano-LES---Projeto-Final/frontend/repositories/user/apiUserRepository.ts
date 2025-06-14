import { UserItem } from '@/domain/models/user/user'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): UserItem {
  return new UserItem(
    item.id,
    item.username,
    item.password,
    item.password_confirmation,
    item.is_superuser,
    item.is_staff,
    item?.first_name,
    item?.last_name,
    item?.email
  )
}

function toPayload(item: UserItem): { [key: string]: any } {
  return {
    id: item.id,
    username: item.username,
    password1: item.password,
    password2: item.passwordConfirmation,
    is_superuser: item.isSuperUser,
    is_staff: item.isStaff,
    first_name: item.first_name ?? '',
    last_name: item.last_name ?? '',
    email: item.email ?? ''
  }
}

export class APIUserRepository {
  constructor(private readonly baseUrl = 'user', private readonly request = ApiService) {}

  async getProfile(): Promise<UserItem> {
    const url = '/me'
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async checkHealth(): Promise<{ status: string; database: string }> {
    const url = '/health'
    const response = await this.request.get(url)
    return response.data
  }

  async checkUserExists(username?: string, email?: string, userId?: number): Promise<{ username_exists?: boolean; email_exists?: boolean }> {
    const url = `/${this.baseUrl}s/check-exists`
    const payload: any = {}
    
    if (username) payload.username = username
    if (email) payload.email = email
    if (userId) payload.user_id = userId
    
    const response = await this.request.post(url, payload)
    return response.data
  }

  async list(username?: string): Promise<UserItem[]> {
    let url = `/${this.baseUrl}s`

    if (username) {
      url += `?search=${encodeURIComponent(username)}`
    }

    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(item: UserItem): Promise<UserItem> {
    const url = `/${this.baseUrl}s/create`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async delete(id: number): Promise<UserItem> {
    const url = `/${this.baseUrl}s/${id}/delete`
    const response = await this.request.delete(url)
    return toModel(response.data)
  }

  async update(id: number, data: Partial<UserItem>): Promise<UserItem> {
    const url = `/${this.baseUrl}s/${id}/update`

    const payload: any = {
      username: data.username,
      first_name: data.first_name ?? '',
      last_name: data.last_name ?? '',
      email: data.email ?? ''
    }

    if (data.password && data.passwordConfirmation) {
      payload.password1 = data.password
      payload.password2 = data.passwordConfirmation
    }

    const response = await this.request.put(url, payload)
    return toModel(response.data)
  }
}
