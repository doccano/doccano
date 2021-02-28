import { MemberItem } from '@/models/member'

export interface MemberItemResponse {
  id: number,
  user: number,
  role: number,
  username: string,
  rolename: string
}

export interface MemberItemListRepository {
  list(projectId: string): Promise<MemberItem[]>

  create(projectId: string, item: MemberItem): Promise<MemberItem>

  update(projectId: string, item: MemberItem): Promise<MemberItem>

  bulkDelete(projectId: string, memberIds: number[]): Promise<void>
}
