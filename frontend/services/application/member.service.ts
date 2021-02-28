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
    const items = await this.repository.list(id)
    return items.map(item => new MemberDTO(item))
  }

  public create(projectId: string, item: MemberDTO): void {
    const member = new MemberItem(0, item.user, item.role, item.username, item.rolename)
    this.repository.create(projectId, member)
  }

  public update(projectId: string, item: MemberDTO): void {
    const member = new MemberItem(item.id, item.user, item.role, item.username, item.rolename)
    this.repository.update(projectId, member)
  }

  public bulkDelete(projectId: string, items: MemberDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }
}
