import { Expose } from 'class-transformer'

export class UserItem {
  id: number;
  username: string;
  
  @Expose({ name: 'is_superuser' })
  isSuperuser: boolean;

  @Expose({ name: 'is_staff' })
  isStaff: boolean;

  toObject(): Object {
    return {
      id: this.id,
      username: this.username,
      is_superuser: this.isSuperuser,
      is_staff: this.isStaff
    }
  }
}
