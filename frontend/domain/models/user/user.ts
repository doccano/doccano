export class User {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly email: string,
    readonly isActive: boolean,
    readonly isSuperUser: boolean,
    readonly isStaff: boolean,
    readonly groups?: number[],
    readonly groupsDetails?: { [key: string]: { name: string } }
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
    readonly isSuperUser: boolean,
    readonly isStaff: boolean,
    readonly dateJoined: string,
    readonly groups?: number[],
    readonly groupsDetails?: { [key: string]: { name: string } }
  ) {
    super(id, username, email, isActive, isSuperUser, isStaff, groups, groupsDetails)
  }
}