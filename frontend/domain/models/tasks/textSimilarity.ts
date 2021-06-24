import { AnnotationModel } from './interface'

export class TextSimilarityItem implements AnnotationModel{
  constructor(
    public id: number,
    public label: number,
    public user: number,
  ) {}

  static valueOf(
    { id, label, user }:
    { id: number, label: number, user: number }
  ) {
    return new TextSimilarityItem(id, label, user)
  }

  toObject() {
    return {
      id: this.id,
      label: this.label,
      user: this.user
    }
  }
}
