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

  toObject(): Object {
    return {
      id: this.id,
      user: this.user,
      role: this.role,
      username: this.username,
      rolename: this.rolename
    }
  }
}
