export class UserItem {
  constructor(
    readonly id: number,
    readonly username: string,
    readonly isSuperuser: boolean,
    readonly isStaff: boolean,
    readonly email?: string,
    readonly sex?: string,
    readonly age?: number
  ) {}
}

// services/user.ts
import { UserItem as User } from './user';

export default class UserService {
  private async get(url: string): Promise<{ data: User }> {
    // Replace with actual HTTP GET implementation
    return fetch(url).then(response => response.json());
  }

  async findById(id: string): Promise<User> {
    const response = await this.get(`/users/${id}`)
    return response.data
  }

  async delete(id: string): Promise<void> {
    await this.delete(`/users/${id}`)
  }
}