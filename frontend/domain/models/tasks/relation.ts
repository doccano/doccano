export class RelationItem {
  constructor(public id: number, public fromId: number, public toId: number, public type: number) {}

  static valueOf({
    id,
    from_id,
    to_id,
    type
  }: {
    id: number
    from_id: number
    to_id: number
    type: number
  }): RelationItem {
    return new RelationItem(id, from_id, to_id, type)
  }

  toObject(): Object {
    return {
      id: this.id,
      from_id: this.fromId,
      to_id: this.toId,
      type: this.type
    }
  }
}
