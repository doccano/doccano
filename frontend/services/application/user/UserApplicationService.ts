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
      // Handle specific validation errors
      if (e.response?.data) {
        const errorData = e.response.data
        
        // Check for field-specific errors
        if (errorData.email && Array.isArray(errorData.email)) {
          throw new Error(`Email: ${errorData.email[0]}`)
        }
        
        if (errorData.username && Array.isArray(errorData.username)) {
          throw new Error(`Username: ${errorData.username[0]}`)
        }
        
        if (errorData.first_name && Array.isArray(errorData.first_name)) {
          throw new Error(`First Name: ${errorData.first_name[0]}`)
        }
        
        if (errorData.last_name && Array.isArray(errorData.last_name)) {
          throw new Error(`Last Name: ${errorData.last_name[0]}`)
        }
        
        // Check for general detail message
        if (errorData.detail) {
          throw new Error(errorData.detail)
        }
        
        // Check for non_field_errors
        if (errorData.non_field_errors && Array.isArray(errorData.non_field_errors)) {
          throw new Error(errorData.non_field_errors[0])
        }
      }
      
      throw new Error(`Failed to update user with ID ${id}`)
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