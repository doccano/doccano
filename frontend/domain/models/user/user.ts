export class UserItem {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly email: string,
    readonly isSuperuser: boolean,
    readonly isStaff: boolean,
    readonly isActive: boolean,
    readonly firstName: string,
    readonly lastName: string
  ) {}
}
