import { AnswerItem } from './answer'

export interface AnswerRepository {
  create(item: AnswerItem): Promise<AnswerItem>
  list(): Promise<AnswerItem[]>
}
