import { RoleName } from '../role/role'

export class MemberItem {
  constructor(
    readonly id: number,
    readonly user: number,
    readonly role: number,
    readonly username: string,
    readonly rolename: RoleName
  ) {}

  get isProjectAdmin(): boolean {
    return this.rolename === 'project_admin'
  }
}
