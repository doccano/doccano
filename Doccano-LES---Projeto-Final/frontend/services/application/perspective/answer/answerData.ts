import { AnswerItem } from '~/domain/models/perspective/answer/answer'

export class AnswerDTO {
  id: number
  member: number
  question: number
  answer_text?: string
  answer_option?: string

  constructor(item: AnswerItem) {
    this.id = item.id
    this.member = item.member
    this.question = item.question
    this.answer_text = item.answer_text
    this.answer_option = item.answer_option
  }
}
