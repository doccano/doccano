import ApiService from '@/services/api.service'
import { MemberRepository } from '@/domain/models/member/memberRepository'
import { MemberItem } from '@/domain/models/member/member'

function toModel(item: { [key: string]: any }): MemberItem {
  return new MemberItem(item.id, item.user, item.role, item.username, item.rolename)
}

function toPayload(item: MemberItem): { [key: string]: any } {
  return {
    id: item.id,
    user: item.user,
    role: item.role,
    username: item.username,
    rolename: item.rolename
  }
}

export class APIMemberRepository implements MemberRepository {
  constructor(private readonly request = ApiService) {}

  async list(projectId: string): Promise<MemberItem[]> {
    const url = `/projects/${projectId}/members`
    const response = await this.request.get(url)
    return response.data.map((item: { [key: string]: any }) => toModel(item))
  }

  async create(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members`
    const payload = toPayload(item)
    const response = await this.request.post(url, payload)
    return toModel(response.data)
  }

  async update(projectId: string, item: MemberItem): Promise<MemberItem> {
    const url = `/projects/${projectId}/members/${item.id}`
    const payload = toPayload(item)
    const response = await this.request.patch(url, payload)
    return toModel(response.data)
  }

  async bulkDelete(projectId: string, memberIds: number[]): Promise<void> {
    const url = `/projects/${projectId}/members`
    await this.request.delete(url, { ids: memberIds })
  }

  async fetchMyRole(projectId: string): Promise<MemberItem> {
    const url = `/projects/${projectId}/my-role`
    const response = await this.request.get(url)
    return toModel(response.data)
  }
}
