import { UserDTO } from './userData'

export type CreateUserCommand = Omit<UserDTO, 'id'>
