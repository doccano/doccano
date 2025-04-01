export class AnswerItem {
  constructor(
    readonly id: number,
    readonly answer: string,
    readonly memberId: number,
    readonly questionId: number
  ) {}

  static create(answer: string, memberId: number, questionId: number): AnswerItem {
    return new AnswerItem(0, answer, memberId, questionId)
  }

  static list(items: { answer: string; memberId: number; questionId: number }[]): AnswerItem[] {
    return items.map((item) => AnswerItem.create(item.answer, item.memberId, item.questionId))
  }
}
