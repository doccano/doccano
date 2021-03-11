export class TextClassificationItem {
  constructor(
    public id: number,
    public label: number,
    public user: number,
  ) {}

  static valueOf(
    { id, label, user }:
    { id: number, label: number, user: number }
  ): TextClassificationItem {
    return new TextClassificationItem(id, label, user)
  }

  toObject(): Object {
    return {
      id: this.id,
      label: this.label,
      user: this.user
    }
  }
}
