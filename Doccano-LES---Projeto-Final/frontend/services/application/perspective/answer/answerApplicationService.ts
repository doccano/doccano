import { AnswerDTO } from './answerData'
import { CreateAnswerCommand } from './answerCommand'
import { AnswerItem } from '~/domain/models/perspective/answer/answer'
import { AnswerRepository } from '~/domain/models/perspective/answer/answerRepository'

export class AnswerApplicationService {
  constructor(private readonly repository: AnswerRepository) {}

  public async create(projectId: string, item: CreateAnswerCommand): Promise<AnswerDTO> {
    const answer = AnswerItem.create(item.member, item.question, item.answer_text, item.answer_option)
    const created = await this.repository.create(projectId, answer)
    return new AnswerDTO(created)
  }

  public async list(): Promise<AnswerItem[]> {
    return await this.repository.list()
  }
}
