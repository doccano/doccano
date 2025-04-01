import { QuestionDTO } from './question/questionData'
import { PerspectiveItem } from '~/domain/models/perspective/perspective'

export class PerspectiveDTO {
  id: number
  project_id: number
  questions: QuestionDTO[]
  members: number[]

  constructor(item: PerspectiveItem) {
    this.id = item.id
    this.project_id = item.project_id
    this.questions = item.questions.map((question) => new QuestionDTO(question))
    this.members = item.members
  }
}
