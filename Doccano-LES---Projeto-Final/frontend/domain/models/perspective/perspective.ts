import { PerspectiveRepository } from './perspectiveRepository'
import { QuestionItem } from './question/question'

export class PerspectiveItem {
  constructor(
    readonly id: number,
    readonly name: string,
    readonly project_id: number,
    readonly questions: QuestionItem[],
    readonly members: number[]
  ) {}

  static create(name: string, project_id: number, questions: QuestionItem[], members: number[]): PerspectiveItem {
    return new PerspectiveItem(0, name, project_id, questions, members)
  }
  
  static async list(repository: PerspectiveRepository, project_id: string): Promise<PerspectiveItem[]>{
    return await repository.list(project_id)
  }
}
