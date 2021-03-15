import { RoleItem } from '@/models/role'


export class RoleDTO {
  id: number;
  rolename: string;

  constructor(item: RoleItem) {
    this.id = item.id;
    this.rolename = item.name;
  }
}
