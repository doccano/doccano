import { AnswerDTO } from './answerData'

export type CreateAnswerCommand = Omit<AnswerDTO, 'id'>

export type ListAnswerCommand = {
  username?: string
}
