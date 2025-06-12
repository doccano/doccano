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

  async register(
    username: string,
    firstName: string,
    lastName: string,
    email: string,
    password: string,
    passwordConfirm: string
  ): Promise<void> {
    const url = '/register'
    await this.request.post(url, { 
      username, 
      first_name: firstName, 
      last_name: lastName, 
      email, 
      password, 
      password_confirm: passwordConfirm 
    })
  }
}
