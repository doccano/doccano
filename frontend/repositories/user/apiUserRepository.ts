import { Page } from '@/domain/models/page'
import { UserItem } from '@/domain/models/user/user'
import ApiService from '@/services/api.service'

function toModel(item: { [key: string]: any }): UserItem {
  return new UserItem(
    item.id,
    item.username,
    item.email,
    item.is_superuser,
    item.is_staff,
    item.is_active,
    item.first_name,
    item.last_name
  )
}



function toPayload(item: { [key: string]: any }): { [key: string]: any } {
  return {
    username: item.username,
    email: item.email,
    password1: item.password1,
    password2: item.password2,
    is_superuser: item.is_superuser,
    is_staff: item.is_staff
  }
}

export class APIUserRepository {
  constructor(private readonly request = ApiService) {}

  async getProfile(): Promise<UserItem> {
    const url = '/me'
    const response = await this.request.get(url)
    return toModel(response.data)
  }

  async list(query: any): Promise<Page<UserItem>> {
    try {
      const queryString = new URLSearchParams(query).toString()
      const url = queryString ? `/users?${queryString}` : `/users`
      const response = await this.request.get(url)

      let results, count, next, prev
      if (Array.isArray(response.data)) {
        results = response.data
        count = results.length
        next = null
        prev = null
      } else {
        results = response.data.results
        count = response.data.count
        next = response.data.next
        prev = response.data.previous
      }

      return new Page(
        count,
        next,
        prev,
        results.map((item: { [key: string]: any }) => toModel(item))
      )
    } catch (error) {
      console.error('Erro ao listar usuários:', error)
      throw error
    }
  }
  
  async bulkDelete(userIds: number[]): Promise<void> {
    const url = '/users/delete'; // nova rota
    await this.request.post(url, { ids: userIds }, { headers: { "Content-Type": "application/json" } });
  }
  
  
  
  
  

  async create(fields: { [key: string]: any }): Promise<UserItem> {
    const url = '/users/create'
    const payload = toPayload(fields)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }
}
