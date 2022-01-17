import { MemberItem } from '~/domain/models/member/member'

export interface MemberRepository {
  list(projectId: string): Promise<MemberItem[]>

  create(projectId: string, item: MemberItem): Promise<MemberItem>

  update(projectId: string, item: MemberItem): Promise<MemberItem>

  bulkDelete(projectId: string, memberIds: number[]): Promise<void>
}
