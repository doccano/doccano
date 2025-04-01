import { AnswerItem } from '~/domain/models/perspective/answer/answer'

export class AnswerDTO {
  id: number
  answer: string
  memberId: number
  questionId: number

  constructor(item: AnswerItem) {
    this.id = item.id
    this.answer = item.answer
    this.memberId = item.memberId
    this.questionId = item.questionId
  }
}
