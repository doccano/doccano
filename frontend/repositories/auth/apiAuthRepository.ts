import ApiService from '@/services/api.service'

export class APIAuthRepository {
  constructor(private readonly request = ApiService) {}

  async login(username: string, password: string): Promise<void> {
    const url = `/auth/login/`
    await this.request.post(url, { username, password })
  }

  async logout(): Promise<void> {
    const url = '/auth/logout/'
    await this.request.post(url)
  }

  async socialLink(): Promise<any[]> {
    const url = '/social/links/'
    const response = await this.request.get(url)
    return response.data
  }
}
