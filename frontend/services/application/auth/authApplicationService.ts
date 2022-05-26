import { AuthRepository } from '~/domain/models/auth/authRepository'

export class AuthApplicationService {
  constructor(private readonly repository: AuthRepository) {}

  public async login(username: string, password: string) {
    await this.repository.login(username, password)
  }

  public async logout() {
    await this.repository.logout()
  }
}
