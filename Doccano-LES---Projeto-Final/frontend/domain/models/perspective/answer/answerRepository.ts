import { AnswerItem } from './answer'

export interface AnswerRepository {
  create(projectId: string, item: AnswerItem): Promise<AnswerItem>
  list(): Promise<AnswerItem[]>
}
