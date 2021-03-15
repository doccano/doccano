import { MemberItem } from '@/models/member'


export class MemberDTO {
  id: number;
  user: number;
  role: number;
  username: string;
  rolename: string;

  constructor(item: MemberItem) {
    this.id = item.id;
    this.user = item.user;
    this.role = item.role;
    this.username = item.username;
    this.rolename = item.rolename;
  }
}
