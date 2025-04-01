import { AnswerDTO } from '../answer/answerData'
import { CreateOptionsQuestionCommand } from './questionCommand'
import {
  OptionsGroupItem,
  QuestionItem,
  QuestionTypeItem
} from '~/domain/models/perspective/question/question'

export class QuestionDTO {
  id: number
  question: string
  type: number
  answers: AnswerDTO[]
  perspective_id?: number
  options_group?: number

  constructor(item: QuestionItem) {
    this.id = item.id
    this.question = item.question
    this.answers = item.answers.map((answer) => new AnswerDTO(answer))
    this.type = item.type
    this.perspective_id = item.perspective_id
    this.options_group = item.options_group
  }
}

export class OptionsQuestionDTO {
  id: number
  option: string
  options_group: number

  constructor(item: OptionsQuestionDTO) {
    this.id = item.id
    this.option = item.option
    this.options_group = item.options_group
  }
}

export class OptionsGroupDTO {
  id: number
  name: string
  options_questions: CreateOptionsQuestionCommand[]

  constructor(item: OptionsGroupItem) {
    this.id = item.id
    this.name = item.name
    this.options_questions = item.options_questions
  }
}

export class QuestionTypeDTO {
  id: number
  question_type: string

  constructor(item: QuestionTypeItem) {
    this.id = item.id
    this.question_type = item.question_type
  }
}
