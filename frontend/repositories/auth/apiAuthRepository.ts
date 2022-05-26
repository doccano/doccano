import ApiService from '@/services/api.service'
import { AuthRepository } from '@/domain/models/auth/authRepository'

export class APIAuthRepository implements AuthRepository {
  constructor(private readonly request = ApiService) {}

  async login(username: string, password: string): Promise<void> {
    const url = `/auth/login/`
    await this.request.post(url, { username, password })
  }

  async logout(): Promise<void> {
    const url = '/auth/logout/'
    await this.request.post(url)
  }
}
