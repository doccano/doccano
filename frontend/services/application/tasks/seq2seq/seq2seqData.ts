import { TextLabel } from '@/domain/models/tasks/seq2seq'

export class Seq2seqDTO {
  id: number
  text: string
  user: number

  constructor(item: TextLabel) {
    this.id = item.id
    this.text = item.text
    this.user = item.user
  }
}
