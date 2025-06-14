import { AnswerItem } from '../answer/answer'
import { OptionsGroupRepository, OptionsQuestionRepository, QuestionRepository } from './questionRepository'
import { CreateOptionsQuestionCommand } from '~/services/application/perspective/question/questionCommand'


export class QuestionItem {
  constructor(
    readonly id: number,
    readonly question: string,
    readonly type: number,
    readonly answers: AnswerItem[],
    readonly perspective_id: number,
    readonly options_group?: number
  ) {}

  static create(
    question: string,
    type: number,
    answers: AnswerItem[] = [],
    perspective_id: number,
    options_group?: number
  ): QuestionItem {
    return new QuestionItem(0, question, type, answers, perspective_id, options_group)
  }

  static list(repository: QuestionRepository, perspectiveId: number, project_id: string): Promise<QuestionItem[]> {
    return repository.list(perspectiveId, project_id)
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

  static list(repository: OptionsGroupRepository, project_id: string): Promise<OptionsGroupItem[]> {
    return repository.list(project_id)
  }
}

export class OptionsQuestionItem {
  constructor(readonly id: number, readonly option: string, readonly options_group: number) {}

  static create(option: string, options_group: number): OptionsQuestionItem {
    return new OptionsQuestionItem(0, option, options_group)
  }

  static async list(repository: OptionsQuestionRepository, project_id: string): Promise<OptionsQuestionItem[]> {
    return await repository.list(project_id)
  }
}

export class QuestionTypeItem {
  constructor(readonly id: number, readonly question_type: string) {}

  static create(question_type: string): QuestionTypeItem {
    return new QuestionTypeItem(0, question_type)
  }
}
