import { plainToInstance } from 'class-transformer'
import { MemberDTO } from './memberData'
import { MemberRepository } from '~/domain/models/member/memberRepository'
import { MemberItem } from '~/domain/models/member/member'

export class MemberApplicationService {
  constructor(
    private readonly repository: MemberRepository
  ) {}

  public async list(id: string): Promise<MemberDTO[]> {
    try {
      const items = await this.repository.list(id)
      return items.map(item => new MemberDTO(item))
    } catch(e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async create(projectId: string, item: MemberDTO): Promise<void> {
    try {
      const member = plainToInstance(MemberItem, item)
      await this.repository.create(projectId, member)
    } catch(e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public async update(projectId: string, item: MemberDTO): Promise<void> {
    try {
      const member = plainToInstance(MemberItem, item)
      await this.repository.update(projectId, member)
    } catch(e: any) {
      throw new Error(e.response.data.detail)
    }
  }

  public bulkDelete(projectId: string, items: MemberDTO[]): Promise<void> {
    const ids = items.map(item => item.id)
    return this.repository.bulkDelete(projectId, ids)
  }

  public async isProjectAdmin(projectId: string): Promise<boolean> {
    const item = await this.repository.fetchMyRole(projectId)
    return item.isProjectAdmin
  }
}
