import { Seq2seqLabel } from '~/domain/models/tasks/seq2seq'

export class Seq2seqDTO {
  id: number
  text: string
  user: number

  constructor(item: Seq2seqLabel) {
    this.id = item.id
    this.text = item.text
    this.user = item.user
  }
}
