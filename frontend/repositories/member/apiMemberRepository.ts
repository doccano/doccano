import ApiService from '@/services/api.service'
import { MemberRepository, MemberItemResponse } from '@/domain/models/member/memberRepository'
import { MemberItem } from '~/domain/models/member/member'


export class APIMemberRepository implements MemberRepository {
  constructor(
    private readonly request = ApiService
  ) {}

  async list(projectId: string): Promise<MemberItem[]> {
    const url = `/projects/${projectId}/members`
    const response = await this.request.get(url)
    const responseItems: MemberItemResponse[] = response.data
    return responseItems.map(item => MemberItem.valueOf(item))
  }

  async create(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members`
    const response = await this.request.post(url, item.toObject())
    const responseItem: MemberItemResponse = response.data
    return MemberItem.valueOf(responseItem)
  }

  async update(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members/${item.id}`
    const response = await this.request.patch(url, item.toObject())
    const responseItem: MemberItemResponse = response.data
    return MemberItem.valueOf(responseItem)
  }

  async bulkDelete(projectId: string, memberIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/members`
    await this.request.delete(url, { ids: memberIds })
  }
}
