import { MemberItem } from '@/models/member'
import { MemberItemListRepository } from '@/repositories/member/interface'

export class MemberDTO {
  id: number
  user: number
  role: number
  username: string
  rolename: string

  constructor(item: MemberItem) {
    this.id = item.id
    this.user = item.user
    this.role = item.role
    this.username = item.username
    this.rolename = item.rolename
  }
}

export class MemberApplicationService {
  constructor(
    private readonly repository: MemberItemListRepository
  ) {}

  public async list(id: string): Promise<MemberDTO[]> {
    try {
      const items = await this.repository.list(id)
      return items.map(item => new MemberDTO(item))
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public async create(projectId: string, item: MemberDTO): Promise<void> {
    try {
      const member = new MemberItem(0, item.user, item.role, item.username, item.rolename)
      await this.repository.create(projectId, member)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(projectId: string, item: MemberDTO): Promise<void> {
    try {
      const member = new MemberItem(item.id, item.user, item.role, item.username, item.rolename)
      await this.repository.update(projectId, member)
    } catch(e) {
      throw new Error(e.response.data.detail)
    }
  }

  public bulkDelete(projectId: string, items: MemberDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }
}
