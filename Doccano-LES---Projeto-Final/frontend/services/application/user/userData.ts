import { UserItem } from '~/domain/models/user/user'

export class UserDTO {
  id: number
  username: string
  password: string
  passwordConfirmation: string
  isSuperUser: boolean
  isStaff: boolean
  first_name?: string
  last_name?: string
  email?: string

  constructor(item: UserItem) {
    this.id = item.id
    this.username = item.username
    this.password = item.password
    this.passwordConfirmation = item.passwordConfirmation
    this.isSuperUser = item.isSuperUser
    this.isStaff = item.isStaff
    this.first_name = item.first_name ?? ''
    this.last_name = item.last_name ?? ''
    this.email = item.email ?? ''
  }
}
