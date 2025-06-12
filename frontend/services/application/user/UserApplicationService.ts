import { User, UserDetails } from '@/domain/models/user/user'
import { APIUserRepository, PaginatedResponse } from '@/repositories/user/apiUserRepository'

type UserUpdateFields = {
  username?: string
  is_superuser?: boolean
  is_staff?: boolean
  groups?: number[]
  [key: string]: any
}

export class UserApplicationService {
  constructor(private readonly repository: APIUserRepository) {}

  public async getProfile(): Promise<User> {
    try {
      return await this.repository.getProfile()
    } catch (e: any) {
      throw new Error(e.response?.data?.detail || 'Failed to fetch user profile')
    }
  }

  public async list(query: string = ''): Promise<PaginatedResponse<User>> {
    try {
      return await this.repository.list(query)
    } catch (e: any) {
      throw new Error(e.response?.data?.detail || 'Failed to fetch users')
    }
  }

  public async getUser(id: number): Promise<UserDetails> {
    try {
      return await this.repository.getUser(id)
    } catch (e: any) {
      throw new Error(e.response?.data?.detail || `Failed to fetch user with ID ${id}`)
    }
  }

  public async updateUser(id: number, data: UserUpdateFields): Promise<User> {
    try {
      return await this.repository.updateUser(id, data)
    } catch (e: any) {
      throw new Error(e.response?.data?.detail || `Failed to update user with ID ${id}`)
    }
  }

  public async deleteUser(id: number): Promise<void> {
    try {
      await this.repository.deleteUser(id)
    } catch (e: any) {
      throw new Error(e.response?.data?.detail || `Failed to delete user with ID ${id}`)
    }
  }
}