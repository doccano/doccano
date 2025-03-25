import { Page } from '~/domain/models/page'
import { UserItem } from '~/domain/models/user/user'
import { APIUserRepository } from '~/repositories/user/apiUserRepository'

type UserFields = {
  username: string
  email: string
  password1: string
  password2: string
}

export interface SearchQueryData {
  limit: string
  offset: string
  q?: string
}

export class UserApplicationService {
  constructor(private readonly repository: APIUserRepository) {}

  public async list(q: SearchQueryData): Promise<Page<UserItem>> {
    try {
      return await this.repository.list(q.q || '')
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async create(fields: UserFields): Promise<UserItem> {
    try {
      return await this.repository.create(fields)
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async getProfile(): Promise<UserItem> {
    try {
      return await this.repository.getProfile()
    } catch (e: any) {
      throw new Error(e.response.data.detail)
    }
}
}