import { AnswerItem } from '../answer/answer'
import { CreateOptionsQuestionCommand } from '~/services/application/perspective/question/questionCommand'

export class QuestionItem {
  constructor(
    readonly id: number,
    readonly question: string,
    readonly type: number,
    readonly answers: AnswerItem[],
    readonly perspective_id?: number,
    readonly options_group?: number
  ) {}

  static create(
    question: string,
    type: number,
    answers: AnswerItem[] = [],
    perspective_id?: number,
    options_group?: number
  ): QuestionItem {
    return new QuestionItem(0, question, type, answers, perspective_id, options_group)
  }
}

export class OptionsGroupItem {
  constructor(
    readonly id: number,
    readonly name: string,
    readonly options_questions: CreateOptionsQuestionCommand[]
  ) {}

  static create(name: string, options_questions: CreateOptionsQuestionCommand[]): OptionsGroupItem {
    return new OptionsGroupItem(0, name, options_questions)
  }
}

export class OptionsQuestionItem {
  constructor(readonly id: number, readonly option: string, readonly options_group: number) {}

  static create(option: string, options_group: number): OptionsQuestionItem {
    return new OptionsQuestionItem(0, option, options_group)
  }
}

export class QuestionTypeItem {
  constructor(readonly id: number, readonly question_type: string) {}

  static create(question_type: string): QuestionTypeItem {
    return new QuestionTypeItem(0, question_type)
  }

  /*
  static list(items: { id: number, question: string, answers: AnswerItem[] }[]): QuestionItem[] {
    return items.map(item => new QuestionItem(item.id, item.question, item.answers))
  }
    */
}
