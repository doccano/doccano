export class UserItem {
  constructor(
    public id: number,
    public username: string,
    public is_superuser: boolean
  ) {}

  static valueOf(
    { id, username, is_superuser }:
    { id: number, username: string, is_superuser: boolean }
  ): UserItem {
    return new UserItem(id, username, is_superuser)
  }

  toObject(): Object {
    return {
      id: this.id,
      username: this.username,
      is_superuser: this.is_superuser
    }
  }
}
