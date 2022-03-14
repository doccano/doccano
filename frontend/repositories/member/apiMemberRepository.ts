import { plainToInstance } from 'class-transformer'
import ApiService from '@/services/api.service'
import { MemberRepository } from '@/domain/models/member/memberRepository'
import { MemberItem } from '~/domain/models/member/member'

export class APIMemberRepository implements MemberRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<MemberItem[]> {
    const url = `/projects/${projectId}/members`
    const response = await this.request.get(url)
    return response.data.map((item: any) => plainToInstance(MemberItem, item))
  }

  async create(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members`
    const response = await this.request.post(url, item.toObject())
    return plainToInstance(MemberItem, response.data)
  }

  async update(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    return plainToInstance(MemberItem, response.data)
  }

  async bulkDelete(projectId: string, memberIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/members`
    await this.request.delete(url, { ids: memberIds })
  }

  async fetchMyRole(projectId: string): Promise<MemberItem> {
    const url = `/projects/${projectId}/my-role`
    const response = await this.request.get(url)
    return plainToInstance(MemberItem, response.data)
  }
}
