export class MemberItem {
  constructor(
    public id: number,
    public user: number,
    public role: number,
    public username: string,
    public rolename: string
  ) {}

  static valueOf(
    { id, user, role, username, rolename }:
    { id: number, user: number, role: number, username: string, rolename: string }
  ): MemberItem {
    return new MemberItem(id, user, role, username, rolename)
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
