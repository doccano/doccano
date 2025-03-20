export class User {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly email: string,
    readonly isActive: boolean,
    readonly isSuperuser: boolean,
    readonly isStaff: boolean,
  ) {}
}

export class UserDetails extends User {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly email: string,
    readonly firstName: string,
    readonly lastName: string,
    readonly isActive: boolean,
    readonly isSuperuser: boolean,
    readonly isStaff: boolean,
    readonly dateJoined: string
  ) {
    super(id, username, email, isActive, isSuperuser, isStaff)
  }
}