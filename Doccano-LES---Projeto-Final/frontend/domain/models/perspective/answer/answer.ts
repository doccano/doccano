import { AnswerRepository } from "./answerRepository";

export class AnswerItem {
  constructor(
    readonly id: number,
    readonly member: number,
    readonly question: number,
    readonly answer_text?: string,
    readonly answer_option?: string
  ) {}

  static create(member: number, question: number, answer_text?: string, answer_option?: string): AnswerItem {
    return new AnswerItem(0, member, question, answer_text, answer_option);
  }

  static async list(AnswerRepository: AnswerRepository): Promise<AnswerItem[]> {
    return await AnswerRepository.list();
  }
}
