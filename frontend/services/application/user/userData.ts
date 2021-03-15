import { UserItem } from '@/models/user'


export class UserDTO {
  id: number;
  username: string;

  constructor(item: UserItem) {
    this.id = item.id;
    this.username = item.username;
  }
}
