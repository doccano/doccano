import { AnnotationModel } from './interface'

export class Seq2seqLabel implements AnnotationModel {
  constructor(public id: number, public text: string, public user: number) {}

  static valueOf({ id, text, user }: { id: number; text: string; user: number }) {
    return new Seq2seqLabel(id, text, user)
  }

  toObject() {
    return {
      id: this.id,
      text: this.text,
      user: this.user
    }
  }
}
