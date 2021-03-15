import { UserItem } from '~/domain/models/user/user'


export class UserDTO {
  id: number;
  username: string;

  constructor(item: UserItem) {
    this.id = item.id;
    this.username = item.username;
  }
}
