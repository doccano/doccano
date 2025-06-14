import { UserRepository } from './userRepository'

export class UserItem {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly password: string,
    readonly passwordConfirmation: string,
    readonly isSuperUser: boolean,
    readonly isStaff: boolean,
    readonly first_name?: string,
    readonly last_name?: string,
    readonly email?: string
  ) {}

  static create(
    username: string,
    password: string,
    passwordConfirmation: string,
    isSuperUser: boolean,
    isStaff: boolean,
    first_name?: string,
    last_name?: string,
    email?: string
  ): UserItem {
    return new UserItem(
      0,
      username,
      password,
      passwordConfirmation,
      isSuperUser,
      isStaff,
      first_name,
      last_name,
      email
    )
  }

  static async list(repository: UserRepository): Promise<UserItem[]> {
    return await repository.list()
  }

  async delete(repository: UserRepository): Promise<void> {
    if (this.id === 0) {
      throw new Error('Não é possível excluir um usuário sem ID válido.')
    }
    await repository.delete(this.id)
  }

  async update(repository: UserRepository): Promise<void> {
    if (this.id === 0) {
      throw new Error('Não é possível atualizar um usuário sem ID válido.')
    }

    if (this.password && this.password !== this.passwordConfirmation) {
      throw new Error('A confirmação de senha não confere.')
    }

    const updatedFields: Record<string, any> = {
      username: this.username,
      first_name: this.first_name,
      last_name: this.last_name,
      email: this.email
    }

    if (this.password) {
      updatedFields.password = this.password
    }

    await repository.update(this.id, updatedFields)
  }
}
