export class UserItem {
  constructor(
    public id: number,
    public username: string,
    public is_superuser: boolean,
    public is_staff: boolean
  ) {}

  static valueOf(
    { id, username, is_superuser, is_staff }:
    { id: number, username: string, is_superuser: boolean, is_staff: boolean }
  ): UserItem {
    return new UserItem(id, username, is_superuser, is_staff)
  }

  toObject(): Object {
    return {
      id: this.id,
      username: this.username,
      is_superuser: this.is_superuser,
      is_staff: this.is_staff
    }
  }
}
