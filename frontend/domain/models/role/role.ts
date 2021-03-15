export class RoleItem {
  constructor(
    public id: number,
    public name: string
  ) {}

  static valueOf(
    { id, name }:
    { id: number, name: string }
  ): RoleItem{
    return new RoleItem(id, name)
  }

  toObject(): Object {
    return {
      id: this.id,
      name: this.name
    }
  }
}
