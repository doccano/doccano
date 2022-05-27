export class RoleItem {
  id: number
  name: string

  toObject(): Object {
    return {
      id: this.id,
      name: this.name
    }
  }
}
