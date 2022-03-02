import { AnnotationModel } from './interface'

export class Span implements AnnotationModel {
  constructor(
    public id: number,
    public label: number,
    public user: number,
    public startOffset: number,
    public endOffset: number
  ) {}

  static valueOf(
    { id, label, user, start_offset, end_offset }:
    { id: number, label: number, user: number, start_offset: number, end_offset: number }
  ) {
    return new Span(id, label, user, start_offset, end_offset)
  }

  toObject() {
    return {
      id: this.id,
      label: this.label,
      user: this.user,
      start_offset: this.startOffset,
      end_offset: this.endOffset
    }
  }
}
