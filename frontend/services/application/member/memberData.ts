import { MemberItem } from '~/domain/models/member/member'
import { RoleName } from '~/domain/models/role/role'
export class MemberDTO {
  id: number
  user: number
  role: number
  username: string
  rolename: RoleName

  constructor(item: MemberItem) {
    this.id = item.id
    this.user = item.user
    this.role = item.role
    this.username = item.username
    this.rolename = item.rolename
  }
}
