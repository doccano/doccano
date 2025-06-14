import { CreateAnswerCommand } from '../answer/answerCommand'
import { OptionsGroupDTO, OptionsQuestionDTO, QuestionDTO } from './questionData'

export type CreateQuestionCommand = Omit<QuestionDTO, 'id'> & {
  answers: CreateAnswerCommand[]
}

export type CreateOptionsGroupCommand = Omit<OptionsGroupDTO, 'id'>

export type CreateOptionsQuestionCommand = Omit<OptionsQuestionDTO, 'id' | 'options_group'>

export type ListQuestionCommand = {
  username?: string
}
