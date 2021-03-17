import { AnnotationModel } from './interface'

export class TextClassificationItem implements AnnotationModel{
  constructor(
    public id: number,
    public label: number,
    public user: number,
  ) {}

  static valueOf(
    { id, label, user }:
    { id: number, label: number, user: number }
  ) {
    return new TextClassificationItem(id, label, user)
  }

  toObject() {
    return {
      id: this.id,
      label: this.label,
      user: this.user
    }
  }
}
