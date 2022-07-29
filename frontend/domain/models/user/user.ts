export class UserItem {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly isSuperuser: boolean,
    readonly isStaff: boolean
  ) {}
}
